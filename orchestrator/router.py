from typing import Literal
from .state import AgentState
from langchain_core.messages import BaseMessage

def route_from_orchestrator(state: AgentState) -> Literal["chat", "planner", "executor", "__end__"]:
    orchestrator_decision: str = state["messages"][-1].content.upper()

    if "CHAT" in orchestrator_decision:
        return "chat"

    if "PLAN" in orchestrator_decision:
        return "planner"
    
    if state.get("plan") and state["current_step_index"] < len(state["plan"]):
        return "executor"
    
    return END


def route_from_executor(state: AgentState) -> Literal["tools", "increment_step"]:
    last_msg: BaseMessage = state["messages"][-1]

    if last_msg.tool_calls:
        return "tools"
    
    return "increment_step"
