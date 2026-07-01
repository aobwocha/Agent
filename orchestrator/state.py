from typing import TypedDict, Annotated, Any, Literal, Optional
from langchain_core.messages import BaseMessage
import operator

class StepResult(TypedDict):
    step: str
    executor_output: Any
    verification: Optional[dict]
    status: Literal["pending", "pass", "fail"]


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: List[str]
    plan_validation: Optional[dict]
    current_step_index: int
    step_results: Annotated[List[StepResult], operator.add]
