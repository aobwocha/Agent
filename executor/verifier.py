import json
from langchain_core.messages import SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompts import VERIFIER_PROMPT
from ..config import MAIN_MODEL
from ..orchestrator.state import AgentState, StepResult

llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model=MAIN_MODEL)

def verifier_node(state: AgentState) -> dict[str, list[StepResult]]:
    step: str = state["plan"][state["current_step_index"]]
    last_result: StepResult = state["step_results"][-1]
    executor_output: str = last_result["executor_output"]

    prompt: str = VERIFIER_PROMPT.format(
        current_step=step,
        executor_output=executor_output
    )

    response: AIMessage = llm.invoke([SystemMessage(content=prompt)])
    verification: dict[str, str] = json.loads(response.content)

    updated_step: StepResult = {
        **last_result,
        "verification": verification,
        "status": verification["status"]
    }

    step_results: list[StepResult] = state["step_results"][:-1] + [updated_step]

    return {
        "step_results": step_results,
        "messages": [response]
    }