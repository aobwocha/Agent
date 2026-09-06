# Agent

A LangGraph agent that routes a user request to either a direct chat reply or a multi-step plan, then executes that plan one step at a time with tool access.

## How it works

Every request enters through an **orchestrator** node, which classifies the request as `CHAT` or `PLAN`:

- **CHAT** requests (greetings, casual questions) go straight to a **chat** node and return an answer.
- **PLAN** requests (multi-step tasks, calculations, real-time lookups) go to a **planner** node, which breaks the request into numbered steps.

Once a plan exists, the orchestrator hands off one step at a time to an **executor** node. The executor can call tools — a calculator and a web search — through a **tools** node, and loops back until the tool call resolves. After each step, an **increment_step** node advances to the next step and returns control to the orchestrator, which repeats the cycle until the plan is done.

```
START → orchestrator ─┬─ CHAT ──────────→ chat ──────┐
                       ├─ PLAN ──────────→ planner ───┤
                       └─ (steps remain) → executor ──┼─→ back to orchestrator
                                              │        │
                                              ├─ tool call → tools → executor
                                              └─ no tool call → increment_step
                                                                    │
                                                                    └─→ back to orchestrator
                                                                        (no work left) → END
```

## Project structure

```
Agent/
├── main.py                 # Builds and runs the LangGraph workflow
├── config.py                # Model configuration
├── langgraph.json           # LangGraph CLI entry point
├── orchestrator/
│   ├── orchestrator.py       # Classifies each request as CHAT or PLAN
│   ├── router.py              # Conditional edges between nodes
│   ├── state.py                # Shared graph state (AgentState, StepResult)
│   └── prompt.py                # Orchestrator's classification prompt
├── planner/
│   ├── planner.py             # Breaks a request into numbered steps
│   ├── prompts.py              # Planner prompt
│   └── validator.py            # Reserved for plan validation (not yet implemented)
├── executor/
│   ├── executor.py            # Runs a single plan step
│   ├── verifier.py             # Checks a step's output against the step (not yet wired into the graph)
│   └── prompts.py               # Executor and verifier prompts
├── chat/
│   └── chat.py                  # Handles direct, non-plan replies
└── tools/
    ├── tools.py                  # Tool registry
    ├── calculator.py              # Evaluates arithmetic expressions
    └── web_search.py               # Searches the web via DuckDuckGo
```

## Prerequisites

- Python 3.10 or later
- A Google Gemini API key (the agent runs on `ChatGoogleGenerativeAI`)

## Installation

```bash
git clone https://github.com/aobwocha/Agent.git
cd Agent
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your Gemini API key:

```
GOOGLE_API_KEY=your-key-here
```

The model name is set in `config.py` (`MAIN_MODEL`). Change it there if you want to run a different Gemini model.

## Usage

Run the graph directly:

```bash
python -m main
```

This runs the sample request in `main.py` and prints each node's output as the graph executes.

To use the LangGraph CLI and inspector instead:

```bash
langgraph dev
```

## Status

This project is under active development. The orchestrator, planner, executor, chat, and tool-calling loop are wired together and runnable. The verifier and plan validator exist but are not yet connected to the graph.

## License

No license has been chosen yet.
