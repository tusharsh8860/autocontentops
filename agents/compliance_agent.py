# def compliance_agent(content):
#     prompt = f"""
#     You are a strict compliance officer.
#     Check for:
#     - misleading claims
#     - exaggerated promises
#     - risky financial language

#     Content:
#     {content}

#     Respond ONLY:
#     issues_found: true/false
#     issues: [list]
#     """
#     return safe_call(prompt)
def compliance_agent(content):
    return call_llm(f"""
Review this marketing content for compliance.
Reply with ONLY these two lines. No other text whatsoever:

issues_found: true/false
issues: [one line summary of issues, or "none"]

Content:
{content}
""", max_tokens=80)  # ← 80 tokens max — physically cannot write an essay