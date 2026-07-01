from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from . import ORCHESTRATOR
from ..config import MAIN_MODEL
from .state import AgentState

llm = ChatGoogleGenerativeAI(model=MAIN_MODEL)

def chat_node(state: AgentState):
    user_query = [msg.content for msg in state["messages"] if msg.type == "human"][-1]
    response = llm.invoke(user_query)

    content = response.content
    if isinstance(content, list):
        content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    
    decision = content.strip().upper()

    return { "messages" : [AIMessage(content=decision)] }