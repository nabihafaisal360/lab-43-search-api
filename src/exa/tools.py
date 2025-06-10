from dotenv import load_dotenv
import os # Import os to check env var

from langchain_exa import ExaSearchResults
from langchain.tools.retriever import create_retriever_tool # Import create_retriever_tool

# Load environment variables from .env file
load_dotenv()

# Optional: Verify key is loaded
exa_api_key = os.getenv("EXA_API_KEY")
if not exa_api_key:
    print("Warning: EXA_API_KEY not found in environment or .env file.")
    print("Please get one from Exa.ai and add it.")
    # You might want to raise an error or exit here if the key is missing
    # For demonstration, we'll continue but it will fail the API call

# Instantiate the ExaSearch retriever
exa_retriever = ExaSearchResults()

# Create the Exa search tool from the retriever
exa_search_tool = create_retriever_tool(
    exa_retriever,
    "exa_search",
    "Searches the web using Exa.ai for relevant information based on a query."
)

# Export the tool
search_tool = exa_search_tool # Export the wrapped tool as search_tool
