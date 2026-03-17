from crewai import Crew, Task
from agents.GymAgent import gym_agent  # Adjust your import path

# Create a task that forces the agent to read, think, and write.
task = Task(
    description="""
    1. Check my profile for any specific goals or stats.
    2. Check what my last workout was.
    3. Based on my last workout, determine what muscle group I should train today.
    4. Design a full workout routine for that muscle group.
    5. Show me the routine. If I approve, log it to the database.
    """,
    expected_output="A structured workout routine and a confirmation that it was logged to the database.",
    agent=gym_agent,
    human_input=True # Pause so you can approve the workout before it logs it
)

crew = Crew(
    agents=[gym_agent],
    tasks=[task]
)

print("Starting Autonomous Gym Agent Test...")
print(crew.kickoff())