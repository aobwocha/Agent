from .calculator import calculator
from .web_search import web_search
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

tools = [calculator, web_search]
tool_node = ToolNode(tools)
    