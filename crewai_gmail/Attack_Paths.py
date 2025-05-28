from crewai import Agent, Task, Crew
from tools import EmailSenderTool, CheckAvailabilityTool
from google_service_utils import get_google_service
import base64
from email.mime.text import MIMEText
import os
from phoenix.otel import register

# Configure Phoenix tracer
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
    tools=[EmailSenderTool(), CheckAvailabilityTool()],
    verbose=True
)

email_summarizer = Agent(
    role='Email Summarizer',
    goal='Summarize the key content of high-priority emails for quick review.',
    backstory='You provide a clear and concise summary of important emails so the user can quickly understand the context.',
    verbose=True
)


# === Step 2: Utility Function ===

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
            "- If Low-A: generate a brief, polite, and professional response to this email, and forward email if necessary.\n"
            "- If Low-B: check if the user is free today via the CheckAvailabilityTool,"
            "then respond accordingly, confirming or explain and suggesting a different time.\n\n"
            f"Email content:\n{email_text}"
        ),
        expected_output="Return only the full email reply text or a 'SKIP' if classification is High.",
        agent=email_responder,
        context=[classification_task]
    )

    summarization_task = Task(
        description=(
            "You are an assistant that summarizes high-priority emails.\n"
            "If the classification is 'High', summarize the key content of the email and send notification to the user.\n"
            "Otherwise, return 'SKIP'.\n\n"
            f"Email content:\n{email_text}"
        ),
        expected_output="A short summary of the email or 'SKIP'.",
        agent=email_summarizer,
        context=[classification_task]
    )

    crew = Crew(
        agents=[email_classifier, email_responder, email_summarizer],
        tasks=[classification_task, response_task, summarization_task]
    )

    results = crew.kickoff()