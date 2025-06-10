from dotenv import load_dotenv
import os

from langchain_linkup import LinkupSearchRetriever
from langchain.tools.retriever import create_retriever_tool

load_dotenv()

# --- IMPORTANT: Check for the API Key ---
# Get the API key using the name specified by Linkup documentation
# Example: Using LINKUP_API_KEY as the name
linkup_api_key = os.getenv("LINKUP_API_KEY")

if not linkup_api_key:
    raise EnvironmentError(
        "Linkup API Key not found. "
        "Please set the correct environment variable (e.g., LINKUP_API_KEY) "
        "in your .env file or environment. Consult Linkup documentation."
    )

try:
    linkup_retriever = LinkupSearchRetriever(depth="standard")
    print("LinkupSearchRetriever initialized successfully.")
except Exception as e:
     raise RuntimeError(f"Failed to initialize LinkupSearchRetriever: {e}")

# --- Create the Linkup Tool from the Retriever ---
# Define the Linkup tool using create_retriever_tool
linkup_tool = create_retriever_tool(
    linkup_retriever,
    "linkup_search",
    "Searches for relevant information using the Linkup API."
)

# --- Export the tool(s) ---
ALL_TOOLS = [linkup_tool]