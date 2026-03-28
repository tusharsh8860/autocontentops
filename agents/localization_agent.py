def localization_agent(content):
    prompt = f"""
    Convert this into Hinglish for Indian Gen Z.
    Keep it natural and engaging.
    {content}
    """
    return safe_call(prompt)
