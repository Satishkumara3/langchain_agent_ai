import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Web Search Tool
def get_search_tool():
    """Returns a Tavily web search tool."""
    return TavilySearchResults(max_results=3)

@tool
def calculator(expression: str) -> str:
    """Useful for when you need to answer questions about math. 
    Input should be a mathematical expression like '2 + 2' or 'sqrt(16) * 5'."""
    try:
        # Using eval safely for basic math
        # In a production environment, use a more secure math parser or PythonREPL
        import math
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        return str(eval(expression, {"__builtins__": None}, allowed_names))
    except Exception as e:
        return f"Error: {str(e)}"

def get_tools():
    """Returns a list of tools available to the agent."""
    return [get_search_tool(), calculator]
