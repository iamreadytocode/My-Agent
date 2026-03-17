from crewai import Crew, Task
from agents.MealAgent import meal_agent  # Adjust your import path

task = Task(
    description="""
    1. Check my user profile to get my current stats and goals.
    2. I want to eat something spicy today. Based on my profile, suggest a meal that fits my goals.
    3. Estimate the calories and macros for this meal.
    4. Show me the breakdown. If I approve, log it to the database.
    """,
    expected_output="A nutritional breakdown of the meal and a confirmation that it was logged to the database.",
    agent=meal_agent,
    human_input=True # Pause so you can approve the meal before it logs it
)

crew = Crew(
    agents=[meal_agent],
    tasks=[task]
)

print("Starting Autonomous Meal Agent Test...")
print(crew.kickoff())