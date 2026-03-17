from crewai import Crew, Task
from agents.CalendarAgent import calendar_agent
from datetime import datetime

# Dynamically grab today's date so the agent always knows when "tomorrow" is
current_date = datetime.now().strftime("%Y-%m-%d")

task = Task(
    description=f"""
    Today is {current_date}. 
    1. Check the calendar for tomorrow to ensure there are no conflicts.
    2. Create a 1-hour gym session at 7 PM tomorrow.
    3. Create a 1-hour meeting at 9 PM tomorrow.
    4. Send an immediate desktop notification summarizing that these events were successfully created.
    """,
    expected_output="Confirmation text stating the events were scheduled and the notification was triggered.",
    agent=calendar_agent
)

crew = Crew(
    agents=[calendar_agent],
    tasks=[task]
)

print(crew.kickoff())