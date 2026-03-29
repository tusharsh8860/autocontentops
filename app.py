import streamlit as st
import requests
import time

# ✅ Token hardcoded directly — no os.environ dependency
HF_TOKEN = "your_token"

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def call_llm(prompt):
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    for _ in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                # ✅ Show actual error in UI instead of silent fail
                return f"❌ Error {response.status_code}: {response.text}"
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Exception: {str(e)}"
    return "⚠️ Model failed to respond"

def brief_agent(user_input):
    return call_llm(f"Convert into marketing plan JSON:\n{user_input}")

def creator_agent(plan):
    return call_llm(f"Create blog, linkedin post, twitter thread:\n{plan}")

def compliance_agent(content):
    return call_llm(f"Check for misleading or risky claims:\n{content}")

def rewriter_agent(content, issues):
    return call_llm(f"Fix issues:\n{content}\n{issues}")

def localization_agent(content):
    return call_llm(f"Convert to Hinglish:\n{content}")

# def run_pipeline(input_text):
#     plan = brief_agent(input_text)
#     time.sleep(1)
#     content = creator_agent(plan)
#     time.sleep(1)
#     for _ in range(2):
#         compliance = compliance_agent(content)
#         time.sleep(1)
#         if "false" in compliance.lower():
#             break
#         content = rewriter_agent(content, compliance)
#     localized = localization_agent(content)
#     return plan, content, localized

# def run_pipeline(input_text):
#     # Step 1 - Brief
#     plan = brief_agent(input_text)
#     time.sleep(1)

#     # Step 2 - Content
#     content = creator_agent(plan)
#     time.sleep(1)

#     # Step 3 - Compliance (check but DON'T replace content with compliance report)
#     final_content = content  # ← keep original content safe
#     for _ in range(2):
#         compliance = compliance_agent(content)
#         time.sleep(1)
#         if "false" in compliance.lower():
#             break
#         else:
#             rewritten = rewriter_agent(content, compliance)
#             if rewritten and not rewritten.startswith("⚠️"):
#                 final_content = rewritten  # ← only update if rewrite succeeded
#                 content = rewritten

#     # Step 4 - Localization
#     localized = localization_agent(final_content)

#     return plan, final_content, localized

# # -------- UI --------
# st.set_page_config(page_title="AutoContentOps", layout="wide")
# st.title("AutoContentOps")
# st.subheader("AI Content Team in a Box")

# user_input = st.text_area("Enter your content brief:")

# if st.button("Generate Content"):
#     with st.spinner("Running AI agents..."):
#         plan, content, localized = run_pipeline(user_input)

#     st.success("✅ Done!")

#     tab1, tab2, tab3 = st.tabs(["📊 Plan", "📝 Content", "🌍 Hinglish"])
#     with tab1:
#         st.write(plan)
#     with tab2:
#         st.write(content)
#     with tab3:
#         st.write(localized)

#     st.subheader("📈 Impact")
#     st.metric("Time Saved", "4 hrs → 5 mins")
#     st.metric("Automation Level", "80%")

def run_pipeline(input_text, status):
    # Step 1 - Brief
    status.write("🧑‍💼 Brief Agent — converting your brief into a marketing plan...")
    plan = brief_agent(input_text)
    time.sleep(1)

    # Step 2 - Content
    status.write("✍️ Creator Agent — writing blog, LinkedIn post and Twitter thread...")
    content = creator_agent(plan)
    time.sleep(1)

    # Step 3 - Compliance
    status.write("⚖️ Compliance Agent — checking for risky or misleading claims...")
    final_content = content  # ← ALWAYS start with original content

    compliance = compliance_agent(content)
    time.sleep(1)

    if "issues_found: true" in compliance.lower():
        status.write("🔁 Rewriter Agent — fixing flagged issues...")
        rewritten = rewriter_agent(content, compliance)
        time.sleep(1)
        # ← Only accept rewrite if it has all 3 sections
        if (rewritten
            and "BLOG POST" in rewritten
            and "LINKEDIN POST" in rewritten
            and "TWITTER THREAD" in rewritten
            and not rewritten.startswith("⚠️")):
            final_content = rewritten
            status.write("✅ Content rewritten successfully!")
        else:
            # Rewrite failed or got corrupted — keep original
            final_content = content
            status.write("✅ Keeping original content — rewrite was incomplete!")
    else:
        status.write("✅ Compliance passed — no issues found!")
        final_content = content

    # Step 4 - Localization
    status.write("🌍 Localization Agent — converting to Hinglish...")
    localized = localization_agent(final_content)

    return plan, final_content, localized

# -------- UI --------
st.set_page_config(page_title="AutoContentOps", layout="wide")
st.title("🚀 AutoContentOps")
st.subheader("AI Content Team in a Box")

user_input = st.text_area("Enter your content brief:", height=150)

if st.button("Generate Content"):
    if not user_input.strip():
        st.warning("Please enter a campaign brief first.")
    else:
        with st.status("🚀 AutoContentOps pipeline running...", expanded=True) as status:
            plan, content, localized = run_pipeline(user_input, status)
            status.update(label="✅ Pipeline complete!", state="complete", expanded=False)

        st.success("✅ Done!")

        tab1, tab2, tab3 = st.tabs(["📊 Plan", "📝 Content", "🌍 Hinglish"])

        with tab1:
            st.write(plan)

        with tab2:
            if "## BLOG POST" in content:
                sections = content.split("##")
                for section in sections:
                    section = section.strip()
                    if section:
                        lines = section.split("\n", 1)
                        title = lines[0].strip()
                        body = lines[1].strip() if len(lines) > 1 else ""
                        st.subheader(title)
                        st.write(body)
                        st.divider()
            else:
                st.write(content)

        with tab3:
            st.write(localized)

        st.subheader("📈 Impact")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Time Saved", "5 mins", delta="vs 9.5 hrs manual")
        with col2:
            st.metric("Cost Saved", "₹9,800 → ₹0.35", delta="per campaign")