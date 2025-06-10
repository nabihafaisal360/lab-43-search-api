
from dotenv import load_dotenv

load_dotenv()

from langchain_google_community import GoogleSearchRun, GoogleSearchAPIWrapper
# First, create the wrapper. It will look for GOOGLE_API_KEY and GOOGLE_CSE_ID
# in your .env file (because of load_dotenv()) or your actual environment.
wrapper = GoogleSearchAPIWrapper()

# Then, pass the wrapper to the tool.
search_tool = GoogleSearchRun(api_wrapper=wrapper)
