
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

from crewai_gmail.google_service_utils import get_google_service


def send_email(to, subject, body_text):
    try:
        service = get_google_service('gmail', 'v1')

        # 构造 MIME 邮件
        message = MIMEText(body_text)
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # 调用 Gmail API 发送邮件
        send_result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return f"✅ Email sent to {to}, message ID: {send_result['id']}"
    except HttpError as error:
        return f"❌ An error occurred: {error}"


class EmailSenderInput(BaseModel):
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")


class CheckAvailabilityInput(BaseModel):
    pass


class EmailSenderTool(BaseTool):
    name: str = "email_sender"
    description: str = "Sends an email to the specified recipient."
    args_schema: Type[BaseModel] = EmailSenderInput

    def _run(self, to: str, subject: str, body: str) -> str:
        return send_email(to, subject, body)


class CheckAvailabilityTool(BaseTool):
    name: str = Field(default="check_availability", description="Name of the tool")
    description: str = Field(
        default="Checks the user's calendar availability for the rest of the day.",
        description="What the tool does"
    )
    args_schema: Type[BaseModel] = CheckAvailabilityInput

    def _run(self, input=None) -> str:
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
        if not events:
            return "User is available for the rest of the day."
        else:
            event_descriptions = "\n".join(
                f"- {event['summary']} from {event['start'].get('dateTime', 'N/A')} to {event['end'].get('dateTime', 'N/A')}"
                for event in events
            )
            return f"User is not fully available today. Here are the scheduled events:\n{event_descriptions}"
