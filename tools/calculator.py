
@tool
def calculator(expression: str) -> str:
    """Safely evaluates a basic mathematical expression. 
    Use this tool whenever the user asks for mathematical calculations."""
    try:
        return str(eval(expression, { "__builtins__": None }, {}))
    except Exception as e:
        return f"Error evaluating expression: { str(e) }"
