# def creator_agent(plan):
#     prompt = f"""
#     Create high-quality marketing content:
#     1. Blog (200 words)
#     2. LinkedIn post
#     3. Twitter thread (3 tweets)

#     Based on:
#     {plan}
#     """
#     return safe_call(prompt)
def creator_agent(plan):
    return call_llm(f"""
You are a senior content creator. Based on the marketing plan below, write exactly THREE pieces of content.

Use EXACTLY this format with these exact headers:

## BLOG POST
Write a 150-word blog post written FOR the customer, not about the company.
- Write in second person ("you", "your")
- Start with a relatable pain point, NOT "In today's fast-paced world"
- Sound like a human talking to a friend
- Mention the app naturally as the solution
- End with a download CTA
                    
## LINKEDIN POST
[First line must be a bold hook — one sentence that stops the scroll.
Then 3-4 short paragraphs. End with a question to drive comments.
Max 150 words. End with exactly 3 hashtags.]
                    
### TWITTER THREAD
Tweet 1/3: [one punchy sentence, under 280 chars, with 2 hashtags]
Tweet 2/3: [one punchy sentence, under 280 chars, with 2 hashtags]
Tweet 3/3: [one punchy sentence, under 280 chars, ends with CTA and hashtag]

STRICT RULES:
- Exactly 3 tweets, no more
- Each tweet under 280 characters total
- No bullet points inside tweets
- No lists inside tweets

Marketing Plan:
{plan}

RULES:
- You MUST write all three sections
- Start directly with ## BLOG POST
- Do NOT write introductions or explanations
- Do NOT write compliance reviews
- Do NOT write recommendations
""", max_tokens=3000)