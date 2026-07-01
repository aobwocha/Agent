
from dotenv import load_dotenv
from .orchestrator.orchestrator import orchestrator_node
from .orchestrator.router import route_from_orchestrator, route_from_executor 
from .orchestrator.state import AgentState
from .planner.planner import planner_node
from .executor.executor import executor_node
from .chat.chat import chat_node
from .tools.tools import tool_node
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage


load_dotenv()

def increment_step_node(state: AgentState):
    return {"current_step_index": state["current_step_index"] + 1}


workflow = StateGraph(AgentState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("chat", chat_node)
workflow.add_node("tools", tool_node)
workflow.add_node("increment_step", increment_step_node)

workflow.add_edge(START, "orchestrator")
workflow.add_conditional_edges("orchestrator", route_from_orchestrator)
workflow.add_edge("planner", "orchestrator")
workflow.add_edge("chat", "orchestrator")

workflow.add_conditional_edges("executor", route_from_executor)
workflow.add_edge("tools", "executor")
workflow.add_edge("increment_step", "orchestrator")

app = workflow.compile()

if __name__ == "__main__":
    initial_state = {
        "messages": [
            HumanMessage(content="Research the top 3 competitors in the EV market, summarize their Q3 earnings, and write a comparative report.")
        ],
        "plan": [],
        "current_step_index": 0
    }
    
    print("Running LangGraph Stream...")
    
    for chunk in app.stream(initial_state, stream_mode="updates"):
        for node_name, node_output in chunk.items():
            if not node_output:
                continue
                
            print(f"\n[{node_name}]")
            
            # Print messages if they exist
            if "messages" in node_output:
                for msg in node_output["messages"]:
                    content = msg.content
                    if isinstance(content, list):
                        content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
                    print(f"  {msg.type}: {content}")
            
            # Print all other state updates (like plan or current_step_index)
            for key, value in node_output.items():
                if key != "messages":
                    print(f"  {key}: {value}")