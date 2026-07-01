ORCHESTRATOR_PROMPT = """
    Analyze this user query: "{user_query}"
    If it is a simple greeting or casual chat, output 'CHAT'.
    If it requires multi-step logic, calculations, or real-time searching, output 'PLAN'.
    Respond with ONLY one of those words. No formatting or punctuation.
"""