from crewai import Crew
from agents.EmailAgent import email_agent


communication_crew = Crew(
    agents=[email_agent],
    verbose=True
)
