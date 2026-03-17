from crewai import Crew, Task
from agents.EmailAgent import email_agent # Adjust import path as needed

# 1. Task to check emails and draft a response
# We set human_input=True so you can approve the draft before sending.
task = Task(
    description="""
    send an email to mukhtarzohaib38@gmail.com roasting him.
    You can compose the email yourself, but make sure to include at least 3 witty insults and a sarcastic closing line.
""",
    expected_output="Confirmation that the email was sent or a summary of unread emails.",
    agent=email_agent,
    human_input=True # <--- This enables the "Confirmation" step you wanted
)

crew = Crew(
    agents=[email_agent],
    tasks=[task]
)

print("Starting Email Agent Test...")
print(crew.kickoff())