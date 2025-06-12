from dotenv import load_dotenv
import os
from langchain_core.tools import tool # Import the tool decorator

from langchain_exa import ExaSearchResults
from langchain_core.documents import Document # Import Document, though might not be directly used if returning string

# Load environment variables from .env file
load_dotenv()

# Optional: Verify key is loaded
exa_api_key = os.getenv("EXA_API_KEY")
if not exa_api_key:
    print("Warning: EXA_API_KEY not found in environment or .env file.")
    print("Please get one from Exa.ai and add it.")

# Instantiate ExaSearchResults once to be used by the tool function
exa_search_instance = ExaSearchResults()

@tool
def exa_search(query: str) -> str:
    """
    Searches the web using Exa.ai for relevant information based on a query.
    Returns formatted snippets including title, URL, and a text snippet.

    Args:
        query: The search query.

    Returns:
        A string containing the formatted search results.
    """
    print(f"\n--- Calling Exa Search Tool ---")
    print(f"Query: '{query}'")

    try:
        # Invoke the ExaSearchResults instance
        search_response = exa_search_instance.invoke(query)

        # ExaSearchResults returns a SearchResponse object
        # The actual search results are typically in the 'results' attribute
        if hasattr(search_response, 'results') and isinstance(search_response.results, list):
            formatted_results = "Exa Search Results:\n"
            if not search_response.results:
                formatted_results += "No results found.\n"
            else:
                for i, res in enumerate(search_response.results):
                    formatted_results += f"{i+1}. Title: {getattr(res, 'title', 'N/A')}\n"
                    formatted_results += f"   URL: {getattr(res, 'url', 'N/A')}\n"
                    # Add a snippet if available. Exa results often have 'text' or 'snippet'
                    content_snippet = getattr(res, 'text', getattr(res, 'snippet', ''))
                    if content_snippet:
                        formatted_results += f"   Snippet: {content_snippet[:200]}...\n"
                    formatted_results += "---\n"
            return formatted_results.strip()
        else:
            return f"Exa Search: Unexpected response format. No 'results' attribute found or it's not a list: {search_response}"

    except Exception as e:
        print(f"Error executing Exa Search: {e}")
        return f"An error occurred while performing Exa search: {e}"

# Export the tool
search_tool = exa_search
