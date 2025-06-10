from langchain.chat_models import init_chat_model
from linkup_agent.tools import linkup_tool

from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools([linkup_tool])