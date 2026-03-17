from crewai import Agent, Task, Crew
from mytools.healthcare_tools import explain_health_topic
from tga import llm

health_agent = Agent(
    role="Medical Assistant",
    goal="Analyze symptoms and give advice",
    backstory="Medical AI assistant trained on WHO guidelines",
    tools=[explain_health_topic],
    llm =llm,
    verbose=True
)

task = Task(
    description="User reports fever and headache.",
    expected_output="Possible causes and advice.",
    agent=health_agent
)

crew = Crew(
    agents=[health_agent],
    tasks=[task]
)

print(crew.kickoff())
