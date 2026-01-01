from google.adk.agents import LlmAgent
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from app.prompts.root_agent import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()
db_url = "../database/agent_sessions.db"

session_service = SqliteSessionService(db_url)
root_agent = LlmAgent(
                        name= "orchestrator_agent",
                        description= "An AI assistant that helps to find and evaluate products online.",
                        instructions=SYSTEM_PROMPT,
                        model= "",
                        tools= [],
                        sub_agents= [],
                    )
