def compliance_agent(content):
    prompt = f"""
    You are a strict compliance officer.
    Check for:
    - misleading claims
    - exaggerated promises
    - risky financial language

    Content:
    {content}

    Respond ONLY:
    issues_found: true/false
    issues: [list]
    """
    return safe_call(prompt)
