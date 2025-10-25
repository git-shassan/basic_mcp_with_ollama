# pip install langchain_community
# pip install fastmcp
# pip install ddgs
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mytool")

def web_search(query: str, max_results: int = 5) -> dict:
    from langchain_community.tools import DuckDuckGoSearchRun
    search = DuckDuckGoSearchRun()
    results=(search.invoke(str(query)))
    # Simulate search results
    return results


@mcp.tool()
def mytool(query: str) -> str:
    # Call the web_search function with the provided arguments
    search_results = web_search(query=query)
    
    # Format the results for output
    output = "Search Results for:"+str(query)+"\n"
    output +=str(search_results)
    return output


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="http", port=8000)
