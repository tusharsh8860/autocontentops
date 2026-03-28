def creator_agent(plan):
    prompt = f"""
    Create high-quality marketing content:
    1. Blog (200 words)
    2. LinkedIn post
    3. Twitter thread (3 tweets)

    Based on:
    {plan}
    """
    return safe_call(prompt)
