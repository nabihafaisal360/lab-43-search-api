# src/firecrawl_agent/tools.py

from dotenv import load_dotenv
import os
import firecrawl as firecrawl_sdk # Changed import to use an alias
from langchain_core.tools import tool # Import the tool decorator

# Load environment variables from .env file
load_dotenv()

# --- IMPORTANT: Initialize Firecrawl Client ---
# Get the API key early and check if it exists
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

if not firecrawl_api_key:
    # Raise an error if the key is missing. Your application shouldn't
    # proceed if a required API key isn't set.
    raise EnvironmentError(
        "FIRECRAWL_API_KEY not found. "
        "Please add FIRECRAWL_API_KEY='your_key_here' to your .env file or environment. "
        "Get a key from Firecrawl.dev"
    )

# Instantiate the Firecrawl client once when this module loads.
# This client instance will be used by the tool function.
try:
    firecrawl_client = firecrawl_sdk.FirecrawlApp(api_key=firecrawl_api_key) # Use the alias
    print("FirecrawlApp initialized successfully for the search tool.")
except Exception as e:
     # Handle potential errors during client initialization (e.g., invalid key format)
     raise RuntimeError(f"Failed to initialize FirecrawlApp: {e}")


# --- Define the Firecrawl Search Function as a LangChain Tool ---

@tool
def firecrawl_search(query: str) -> str:
    """
    Searches the Firecrawl index for relevant web pages based on a query.
    This tool is useful for finding existing content on a topic within Firecrawl's dataset.

    Args:
        query: The search query.

    Returns:
        A string containing the titles and URLs of the top search results,
        or a message indicating no results were found or an error occurred.
    """
    print(f"\n--- Calling Firecrawl Search Tool ---")
    print(f"Query: '{query}'")

    try:
        # Use the shared firecrawl_client instance
        # We'll request a few results (e.g., top 5)
        # Firecrawl search results are structured (list of objects)
        raw_search_results = firecrawl_client.search(query, limit=int(5))
        
        # Access the 'data' attribute which contains the list of results
        search_results_list = raw_search_results.data

        if not search_results_list:
            print("Firecrawl Search: No results found.")
            return "No results found in the Firecrawl index for this query."

        # Format the structured results into a single string that the LLM can easily read
        formatted_results = "Firecrawl Search Results:\n"
        for i, res in enumerate(search_results_list):
            formatted_results += f"{i+1}. Title: {res.get('title', 'N/A')}\n"
            formatted_results += f"   URL: {res.get('url', 'N/A')}\n"
            # Optionally include a snippet if available
            # if hasattr(res, 'snippet') and res.snippet:
            #     formatted_results += f"   Snippet: {res.snippet[:150]}...\n" # Truncate snippet
            formatted_results += "---\n" # Separator for clarity

        print(f"Firecrawl Search: Found {len(search_results_list)} results.")
        # Return the formatted string, removing any trailing separator
        return formatted_results.strip()

    except Exception as e:
        # If an error occurs during the API call, return an error message
        print(f"Error executing Firecrawl Search: {e}")
        return f"An error occurred while searching the Firecrawl index: {e}"




# It's often helpful to export a list of all tools from this file
ALL_TOOLS = [firecrawl_search]
# If you added the scrape tool:
# ALL_TOOLS = [firecrawl_search, firecrawl_scrape_url]