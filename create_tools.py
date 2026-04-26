from langchain.tools import tool
from langchain_core.tools import BaseTool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for the given query and return the title, urls and snippets."""
    response = tavily.search(query=query, num_results=5)
    results = []
    for result in response['results']:
        title = result['title']
        url = result['url']
        snippet = result['content']
        results.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet[:150]}\n")
    return "\n".join(results)

@tool
def web_scrape(url: str) -> str:
    """Scrape the content of the given URL and return the text for deeper reading."""
    try:
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()
        text = soup.get_text()
        return text[:3000]  # Return only the first 3000 characters
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"