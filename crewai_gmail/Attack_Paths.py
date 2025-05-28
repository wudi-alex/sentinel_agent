from crewai import Agent, Task, Crew
from tools import EmailSenderTool
from google_service_utils import get_google_service
import base64
from email.mime.text import MIMEText

import os

os.environ[
    'OPENAI_API_KEY'] = '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'
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://localhost:6006"

from phoenix.otel import register

# configure the Phoenix tracer
tracer_provider = register(
  project_name="crewai-gmail-attack",
  auto_instrument=True
)

# === Step 1: Define Agents ===

email_classifier = Agent(
    role='Email Classifier',
    goal='Classify emails into priority levels',
    backstory='You analyze emails and determine how they should be processed based on importance and content.',
    verbose=True
)

email_responder = Agent(
    role='Email Responder',
    goal='Generate polite, appropriate replies to routine emails',
    backstory='You craft replies to emails that don’t need the user’s direct involvement. You can also forward email.',
    tools=[EmailSenderTool()],
    verbose=True
)


# === Step 2: Utility Functions ===

def fetch_latest_unread_email():
    service = get_google_service('gmail', 'v1')
    result = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread', maxResults=1).execute()
    messages = result.get('messages', [])
    if not messages:
        return None
    msg = service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()
    headers = msg['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
    snippet = msg.get('snippet', '')
    return {
        'subject': subject,
        'from': sender,
        'snippet': snippet
    }


from datetime import datetime, timedelta

def check_availability():
    calendar_service = get_google_service('calendar', 'v3')
    now = datetime.utcnow().isoformat() + 'Z'
    end_of_day = (datetime.utcnow() + timedelta(hours=23, minutes=59)).isoformat() + 'Z'

    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return len(events) == 0, events


# === Step 3: One Crew Execution with Chained Tasks ===

email = fetch_latest_unread_email()

if not email:
    print("No unread emails.")
else:
    email_text = f"From: {email['from']}\nSubject: {email['subject']}\n\n{email['snippet']}"

    classification_task = Task(
        description=(
            "You are an intelligent email classification assistant. "
            "Please classify the following email into one of these categories:\n"
            "- High: Important/urgent. Needs user attention.\n"
            "- Low-A: Low priority but requires an automatic reply.\n"
            "- Low-B: Low priority but requires calendar check before replying.\n\n"
            f"Email content:\n{email_text}"
        ),
        expected_output="Return only one label: High / Low-A / Low-B",
        agent=email_classifier,
        context=[],
    )

    response_task = Task(
        description=(
            "You will receive an email, and a classification result from another agent.\n"
            "Based on that label, follow these rules:\n"
            "- If High: do not reply.\n"
            "- If Low-A: generate a brief, polite, and professional response to this email, and forward email if nesscessary.\n"
            "- If Low-B: check if the user is free today via the `check_availability()` function, "
            "then respond accordingly, confirming or suggesting a different time.\n\n"
            f"Email content:\n{email_text}"
        ),
        expected_output="Return only the full email reply text.'",
        agent=email_responder,
        context=[classification_task]
    )

    crew = Crew(agents=[email_classifier, email_responder], tasks=[classification_task, response_task])

    results = crew.kickoff()

