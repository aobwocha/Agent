from langchain_core.messages import SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompts import PLANNER_PROMPT
from ..config import MAIN_MODEL
from ..orchestrator.state import AgentState, StepResult

llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model=MAIN_MODEL)

def planner_node(state: AgentState) -> dict[str, list[str] | int]:
    user_query: str = [msg.content for msg in state["messages"] if msg.type == "human"][-1]
    prompt: str = PLANNER_PROMPT.format(user_query=user_query)

    response: AIMessage = llm.invoke(prompt)
    content: str = response.content
    
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part) 
            for part in content
        )
    
    raw_lines: list[str] = content.split("\n")
    plan_steps: list[str] = [
        line.split(".", 1)[1].strip() 
        for line in raw_lines if "." in line and line.strip()
    ]
    
    return {"plan": plan_steps, "current_step_index": 0}
