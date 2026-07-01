EXECUTOR_PROMPT = """
    You are an executor.

    Your job is to complete the given step.

    STEP:
    {current_step}

    Return a clear result for this step only.
"""


VERIFIER_PROMPT = """
    You are a strict verifier.

    STEP:
    {current_step}

    EXECUTOR OUTPUT:
    {executor_output}

    Decide if the output fully satisfies the step.

    Return JSON ONLY:
    {
    "status": "pass" | "fail",
    "issues": [],
    "reason": "...",
    "suggested_fix": "..."
    }
"""