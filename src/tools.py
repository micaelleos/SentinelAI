from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
import dotenv
import os
import requests

dotenv.load_dotenv()

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
tavily_tool = TavilySearchResults(max_results=5,tavily_api_key=TAVILY_API_KEY, topic='news',search_depth="advanced")

from langchain_core.tools import tool

@tool(response_format="content_and_artifact")
def general_search_tool(query: str):
    """A search engine optimized for comprehensive, accurate, and trusted results. 
    Useful for when you need to answer questions about current events. 
    Input should be a search query."""
    client = TavilyClient(TAVILY_API_KEY)

    response = client.search(query=query,search_depth='advanced',max_results=10)
    
    serialized = f"Termos de busca: {query} \n" f"Resultado de Busca: {response}"
    
    return serialized, response

tools_planner = [general_search_tool]


from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader

proxies = {
  "http": "http://zqF7vrzr61igCX4R:74DbvK4zabvQhAL6@geo.g-w.info:10080",
  "https": "http://zqF7vrzr61igCX4R:74DbvK4zabvQhAL6@geo.g-w.info:10080",
}

@tool(response_format="content_and_artifact")
def news_search_tool(query: str):
  """A search engine optimized for comprehensive, accurate, and trusted results. 
  Useful for when you need to answer questions about current events. 
  Input should be a search query."""
  client = TavilyClient(TAVILY_API_KEY,proxies=proxies) #
  response = client.search(query=query,max_results=10)
  serialized = f"Termos de busca: {query} \n" f"Resultado de Busca: {response}"
  
  return serialized, response

@tool(response_format="content_and_artifact")
def read_article(url:str):
  """Use essa ferramenta para ler o artigo na web"""
  loader = WebBaseLoader(url)
  text = loader.load()
  serialized = f"metadados : {text[0].metadata} \n" f"Extração web: {text[0].page_content}"

  return serialized, text[0].page_content

tools_researcher = [news_search_tool, read_article]


@tool
def read_news(url:str):
    """Use essa ferramentas para ler artigos na internet"""
    url1 = f"https://r.jina.ai/{url}"

    headers = {
        "Accept": "application/json",
        "X-Return-Format": "markdown",
        "X-Timeout": "10"
    }

    response = requests.get(url1, headers=headers)

    return response.json()['data']


tool_reader = [read_news]
