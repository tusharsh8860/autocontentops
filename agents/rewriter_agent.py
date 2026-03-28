def rewriter_agent(content, issues):
    prompt = f"""
    Fix all issues while preserving meaning.
    Content:
    {content}
    Issues:
    {issues}
    """
    return safe_call(prompt)
