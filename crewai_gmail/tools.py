from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

from crewai_gmail.gmail_utils import get_gmail_service


def send_email(to, subject, body_text):
    try:
        service = get_gmail_service()

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


class EmailSenderTool(BaseTool):
    name: str = "email_sender"
    description: str = "Sends an email to the specified recipient."
    args_schema: Type[BaseModel] = EmailSenderInput

    def _run(self, to: str, subject: str, body: str) -> str:
        # 实现发送邮件的逻辑
        return send_email(to, subject, body)


# # 发送一封测试邮件
# print(send_email("dwu25@gmu.edu", "Test Subject", "This is the body of the email."))




