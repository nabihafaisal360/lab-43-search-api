from dotenv import load_dotenv
import os # Import os to check env var
from langchain_core.tools import Tool # Import Tool
from langchain_community.utilities import SerpAPIWrapper

# Load environment variables from .env file
load_dotenv()

# Optional: Verify key is loaded
serp_api_key_env = os.getenv("SERPAPI_API_KEY") # Check for SERPAPI_API_KEY
if not serp_api_key_env:
    print("Warning: SERPAPI_API_KEY not found in environment or .env file.") # Warn for SERPAPI_API_KEY
    # You might want to raise an error or exit here if the key is missing

# Create the wrapper. It will look for SERPAPI_API_KEY in your environment.
serpapi = SerpAPIWrapper() # SerpAPIWrapper expects SERPAPI_API_KEY

# Then, define the search_tool using the Tool class
search_tool = Tool(
    name="SerpAPISearch",
    func=serpapi.run,
    description="A search engine. Useful for when you need to answer questions about current events or general information. Input should be a search query."
)