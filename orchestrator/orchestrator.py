from typing import Any
from langchain_core.messages import SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config import MAIN_MODEL
from .state import AgentState
from .prompt import ORCHESTRATOR_PROMPT

llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model=MAIN_MODEL)

def orchestrator_node(state: AgentState) -> dict[str, list[AIMessage]]:
    user_query: str = [msg.content for msg in state["messages"] if msg.type == "human"][-1]
    prompt: str = ORCHESTRATOR_PROMPT.format(user_query=user_query)

    response: AIMessage = llm.invoke(prompt)
    content: str | list[str | dict[Any, Any]] = response.content

    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part) 
            for part in content
        )
    final_content: str = str(content).strip().upper()

    return { "messages" : [AIMessage(content=final_content)] }