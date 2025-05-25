import os.path
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 定义访问 Gmail 发送/读取、Calendar 读取的权限范围
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]


# 获取 Google API 凭据，并返回构建 Gmail/Calendar 服务
def get_google_service(service_name: str, version: str):
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build(service_name, version, credentials=creds)


# 获取 Gmail 中未读邮件（最多10封）
def fetch_unread_emails():
    gmail_service = get_google_service('gmail', 'v1')
    results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    email_texts = []

    for message in messages[:10]:
        msg = gmail_service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        snippet = msg['snippet']
        email_texts.append(snippet)

    return email_texts


# 获取今天的 Calendar 事件
def get_today_calendar_events():
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
    return events


# 主函数：测试两个功能
if __name__ == '__main__':
    print("📧 Unread Gmail Snippets:")
    emails = fetch_unread_emails()
    for i, email in enumerate(emails):
        print(f"{i + 1}. {email}\n")

    print("\n🗓️ Today's Calendar Events:")
    calendar_events = get_today_calendar_events()
    if not calendar_events:
        print("No events found today.")
    else:
        for event in calendar_events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"- {start}: {event.get('summary', 'No title')}")
