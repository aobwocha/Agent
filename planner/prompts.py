PLANNER_PROMPT = """
    Create a step-by-step execution plan to solve this user request: "{user_query}"
    Break it down into simple, atomic tasks.
    Return the plan as a line-separated list where each line starts with a number.
    Example format:
    1. Search for X
    2. Calculate Y based on X
"""