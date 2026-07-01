from langchain_core.messages import SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompts import EXECUTOR_PROMPT
from ..config import MAIN_MODEL
from ..orchestrator.state import AgentState, StepResult

llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model=MAIN_MODEL)

def executor_node(state: AgentState) -> dict[str, list[StepResult | AIMessage]]:
    step: str = state["plan"][state["current_step_index"]]
    user_query: str = [msg.content for msg in state["messages"] if msg.type == "human"][-1]
    system_instruction: str = EXECUTOR_PROMPT.format(current_step=step)
    prompt: list[str] = [system_instruction] + [user_query]

    response: AIMessage = llm.invoke([SystemMessage(content=prompt)])
    content: str | list[str | dict[Any, Any]] = response.content

    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part) 
            for part in content
        )
    final_content: str = str(content).strip().upper()

    step_result: StepResult = StepResult(
        step=step,
        executor_output=final_content,
        verification=None,
        status="pending"
    )

    return {
        "step_results": [step_result],
        "messages": [AIMessage(content=final_content)]
    }