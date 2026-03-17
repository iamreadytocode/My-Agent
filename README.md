Viki: Autonomous Agentic Personal Assistant
Viki is an intelligent, agentic AI system designed to handle personal workflows autonomously. Built with a modular "brain" architecture, it coordinates specialized agents for health, productivity, and communication.

🚀 Features
Orchestrator Brain: High-level reasoning to delegate tasks to specific sub-agents.

Multi-Agent Ecosystem: Dedicated agents for Calendar, Email, Health, and News.

Memory Management: Persistent state using ChromaDB to remember user preferences.

Voice Interface: Integrated Piper models for high-fidelity text-to-speech.

🛠️ Tech Stack
Language: Python 3.10+

AI Framework: CrewAI / LangChain (for agent orchestration)

Database: SQLite (Relational) & ChromaDB (Vector)

Interface: Custom Python-based Views (Onboarding, Login, Chat)

💻 Getting Started
1. Prerequisites
Ensure you have Python installed, then clone the repository:

Bash
git clone https://github.com/iamreadytocode/My-Agent.git
cd My-Agent
2. Environment Setup
Create a virtual environment and install dependencies:

Bash
python -m venv venv
source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Credentials & API Keys
This project requires Google OAuth credentials.

Obtain a credentials.json from the Google Cloud Console.

Place credentials.json in the root directory.

Create a .env file and add your LLM API keys:

Code snippet
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
(Note: credentials.json and .env are ignored by Git for security.)

4. Running the Application
Launch the orchestrator to start the Viki engine:

Bash
python main.py
🏗️ Project Architecture
The system follows a modular design to ensure scalability:

/agents: Logic for specialized autonomous agents.

/crews: Task-specific groupings (e.g., health_crew, productivity_crew).

/llm: The core reasoning engine and agentic brain.

/mytools: Custom tools for Google API and system integration.

/voice: Text-to-speech models and managers.