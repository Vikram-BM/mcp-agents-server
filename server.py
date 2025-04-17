# server.py  (same code as before — keeps everything self‑contained)
from fastmcp import FastMCP
import httpx
from pydantic import BaseModel, Field

mcp = FastMCP("ASU Class Search 🔎")

API = "https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/classes"

class SearchParams(BaseModel):
    term: int = Field(2257, description="ASU term code (e.g. 2257 = Fall 2025)")
    keywords: str | None = Field(None, description="Free‑text keywords")

@mcp.tool()
async def search_asu_classes(params: SearchParams) -> dict:
    q = {
        "refine": "Y",
        "campusOrOnlineSelection": "A",
        "honors": "F",
        "promod": "F",
        "searchType": "all",
        "term": params.term,
    }
    if params.keywords:
        q["keywords"] = params.keywords
    async with httpx.AsyncClient() as c:
        r = await c.get(API, params=q, timeout=30)
        r.raise_for_status()
        return r.json()

if __name__ == "__main__":
    mcp.run("sse", host="0.0.0.0", port=8000)

