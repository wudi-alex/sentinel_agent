from crewai import Agent, Task, Crew
from tools import EmailSenderTool
from gmail_utils import get_gmail_service
import base64
from email.mime.text import MIMEText

import os
os.environ['OPENAI_API_KEY'] = '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'
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

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


# === Step 2: Utility to fetch the latest unread email ===

def fetch_latest_unread_email():
    service = get_gmail_service()
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


# === Step 3: Main execution flow ===

email = fetch_latest_unread_email()

if not email:
    print("No unread emails.")
else:
    email_text = f"From: {email['from']}\nSubject: {email['subject']}\n\n{email['snippet']}"

    # 3a. Classification task
    classification_task = Task(
        description=(
            "You are an intelligent email classification assistant. "
            "Please classify the following email into one of these categories:\n"
            "- High: Important/urgent. Needs user attention.\n"
            # "- Low-A: Low priority. Ignore (promo/notification).\n"
            "- Low-A: Low priority but requires an automatic reply.\n"
            "- Low-B: Low priority but requires calendar check before replying.\n\n"
            "Email content:\n" + email_text
        ),
        expected_output="Return only one label: High / Low-A / Low-B ",
        agent=email_classifier
    )

    crew1 = Crew(agents=[email_classifier], tasks=[classification_task])
    output = crew1.kickoff()
    classification_result = output.raw

    print(f"\nClassification result: {classification_result}")

    # 3b. If classified as Low-B, generate and send reply
    if classification_result == 'Low-A':
        response_task = Task(
            description=f"Generate a brief, polite, and professional response to this email:\n\n{email_text}",
            expected_output="Return only the full email reply text.",
            agent=email_responder
        )

        crew2 = Crew(agents=[email_responder], tasks=[response_task])
        response_text = crew2.kickoff()

    else:
        print("No reply needed for this email.")
