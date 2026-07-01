from duckduckgo_search import DDGS 

@tool
def web_search(query: str) -> str:
    """Searches the web to answer real-time, current, or factual questions.
    Use this tool when the user asks about recent events or information you do not know."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query=query, max_results=3))
            
            if not results:
                return "No explicit search results found. Try a broader search query."
                
            return "\n\n".join([r.get("body", "") for r in results if "body" in r])
    except Exception as e:
        return f"Search encountered an error: {str(e)}"
