import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("campaign-insights-mcp")

FUNCTION_URL = os.getenv(
    "CAMPAIGN_INSIGHTS_FUNCTION_URL",
    "https://func-campaign-insights-uks01.azurewebsites.net/api/getcampaigninsights",
)

API_KEY = os.getenv("MCP_API_KEY")  # optional simple auth

def _auth_ok(headers) -> bool:
    if not API_KEY:
        return True  # auth disabled
    return headers.get("x-api-key") == API_KEY

@mcp.tool()
def get_campaign_insights(question: str) -> dict:
    """
    Get campaign insights using RAG (Azure AI Search + Foundry) via the Azure Function.
    Input: question (string)
    Output: { rag: {summary, keyPoints, recommendations}, citations: [...] }
    """
    r = requests.get(FUNCTION_URL, params={"q": question}, timeout=60)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    # Run as a remote MCP server (HTTP transport) for Copilot Studio
        mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        path="/mcp",
    )

