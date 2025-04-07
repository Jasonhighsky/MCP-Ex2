from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import os

from bs4 import BeautifulSoup
import json

load_dotenv()

mcp = FastMCP("daum_news")
USER_AGENT = "new-app/1.0"
NEWS_SITES = {
    '다음뉴스' : "https://news.daum.net/"
}

async def fetch_news(url: str) :
    """다음뉴스 사이트에서 최신 뉴스를 가져와서 개략적으로 소개합니다."""
    async with httpx.AsyncClient() as client :
        try :
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs[:10]])
            return text
        except httpx.TimeoutException:
            return "Timeout error"
        
@mcp.tool()
async def get_tech_news(source: str) :
    """
    뉴스를 가져와 정리해줌.
    
    Args:
    소스: 다음뉴스
    
    Returns:
    최신 뉴스를 개략적으로 정리 해줌.
    """
    if source not in NEWS_SITES:
        raise ValueError(f"Source {source} is not supported")
    news_text = await fetch_news(NEWS_SITES[source])
    return news_text
            
            
if __name__ == "__main__":
    mcp.run(transport="stdio")