def brief_agent(user_input):
    prompt = f"""
    You are a marketing strategist.
    Convert into JSON:
    - audience
    - tone
    - platforms
    - goals

    Input:
    {user_input}
    """
    return safe_call(prompt)