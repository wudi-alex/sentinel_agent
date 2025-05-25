from crewai import Agent, Task, Crew
from google_service_utils import fetch_unread_emails
from openai import OpenAI

# 你需要设置 OPENAI_API_KEY 环境变量或在代码中传入
import os
os.environ['OPENAI_API_KEY'] = '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'

# Define the email classifier agent
email_classifier = Agent(
    role='Email Classifier',
    goal='Classify emails based on their content into categories: High',
    backstory='You are a highly skilled virtual assistant trained in understanding and organizing email content. You can quickly read and categorize emails with high accuracy.',
    verbose=True
)

# Fetch unread email snippets
emails = fetch_unread_emails()

# Define classification tasks for each email
classification_tasks = [
    Task(
        description=(
            f"Read the following email snippet and classify it into one of the categories: "
            f"Work, Promotion, or Personal.\n\nEmail:\n'{email}'"
        ),
        expected_output='Only return the category name: Work / Promotion / Personal',
        agent=email_classifier
    )
    for email in emails
]

# Run the crew
crew = Crew(
    agents=[email_classifier],
    tasks=classification_tasks
)

results = crew.kickoff()

# Print classification results
for i, result in enumerate(results):
    print(f"\n📩 Email {i+1} classified as: {result}")