# def rewriter_agent(content, issues):
#     prompt = f"""
#     Fix all issues while preserving meaning.
#     Content:
#     {content}
#     Issues:
#     {issues}
#     """
#     return safe_call(prompt)
def rewriter_agent(content, issues):
    return call_llm(f"""
Rewrite the content below fixing ONLY the listed issues.
Keep the exact same format: Blog Post, LinkedIn Post, Twitter Thread.
Do not add recommendations or action plans. Just the rewritten content.

Issues to fix:
{issues}

Original content:
{content}
""", max_tokens=3000)