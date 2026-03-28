# Architecture Document — AutoContentOps

## 1. System Overview

AutoContentOps is a sequential multi-agent pipeline built on a single LLM (Llama 3.1 8B via Hugging Face). Each agent is a specialized prompt wrapper that receives output from the previous stage and transforms it. The system runs server-side via a Streamlit web app, optionally exposed publicly through ngrok.

The pipeline follows a **linear orchestration pattern**: no agent communicates directly with another. Instead, the `run_pipeline()` orchestrator in `app.py` passes outputs as string arguments between agents — keeping coupling minimal and the system easy to debug and extend.

---

## 2. Pipeline Flow

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Browser)                        │
│              Enters campaign brief in UI                 │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  STREAMLIT APP (app.py)                  │
│               run_pipeline(input_text)                   │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────▼─────────────┐
          │       BRIEF AGENT         │
          │  Input:  raw user text    │
          │  Output: JSON plan        │
          │  Persona: Marketing       │
          │          Strategist       │
          └─────────────┬─────────────┘
                        │
          ┌─────────────▼─────────────┐
          │      CREATOR AGENT        │
          │  Input:  JSON plan        │
          │  Output: Blog + LinkedIn  │
          │          + Twitter thread │
          │  Persona: Content Writer  │
          └─────────────┬─────────────┘
                        │
          ┌─────────────▼─────────────┐
          │    COMPLIANCE AGENT       │◄──┐
          │  Input:  content string   │   │ loop (max 2x)
          │  Output: issues_found:    │   │
          │          true/false       │   │
          └──────┬──────────┬─────────┘   │
                 │          │             │
           false │    true  │             │
                 │          ▼             │
                 │  ┌───────────────┐     │
                 │  │ REWRITER AGENT│─────┘
                 │  │ Fixes issues  │
                 │  └───────────────┘
                 │
          ┌──────▼──────────────────────┐
          │    LOCALIZATION AGENT        │
          │  Input:  compliant content   │
          │  Output: Hinglish version    │
          │  Persona: Hinglish Copywriter│
          └─────────────┬───────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  STREAMLIT UI                            │
│        Tab 1: Plan | Tab 2: Content | Tab 3: Hinglish    │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Agent Roles

| Agent | Input | Output | Prompt Persona | Max Tokens |
|-------|-------|--------|----------------|------------|
| Brief Agent | Raw user brief (plain text) | JSON: audience, tone, platforms, goals, budget | Marketing Strategist | 2000 |
| Creator Agent | JSON plan | Blog (200w) + LinkedIn post + Twitter thread (3 tweets) | Senior Content Writer | 3000 |
| Compliance Agent | Generated content | `issues_found: true/false` + issues list | Strict Compliance Officer | 1000 |
| Rewriter Agent | Content + issues list | Rewritten content with all issues resolved | Editor preserving intent | 3000 |
| Localization Agent | Final compliant content | Natural Hinglish for Indian Gen Z | Hinglish Copywriter | 3000 |

---

## 4. Agent Communication

Agents are stateless functions. Communication is handled by `run_pipeline()`:

```python
def run_pipeline(input_text):
    plan       = brief_agent(input_text)        # Step 1
    content    = creator_agent(plan)             # Step 2

    for _ in range(2):                           # Step 3 — compliance loop
        compliance = compliance_agent(content)
        if "false" in compliance.lower():
            break
        content = rewriter_agent(content, compliance)

    localized  = localization_agent(content)     # Step 4
    return plan, content, localized
```

Each agent receives a plain string and returns a plain string. This design means:
- Any agent can be swapped out without touching the others
- Each agent is independently unit-testable
- Adding a new agent requires one function + one line in `run_pipeline()`

---

## 5. LLM Integration

All agents share a single `call_llm()` function in `utils/llm.py`:

```
User Prompt
    ↓
call_llm(prompt, max_tokens)
    ↓
POST https://router.huggingface.co/v1/chat/completions
    ↓
model: meta-llama/Llama-3.1-8B-Instruct:novita
    ↓
Response → agent returns content string
```

**Retry logic:** 3 attempts with 2-second backoff on failure or non-200 response.

---

## 6. Tool Integrations

| Tool | Role | Method |
|------|------|--------|
| Hugging Face Inference Router | LLM backend | REST API (POST /v1/chat/completions) |
| Llama 3.1 8B (novita provider) | Language model for all agents | Model ID in request payload |
| Streamlit | Web UI framework | Python library |
| ngrok / pyngrok | Public URL tunnel | Python library wrapping ngrok binary |
| python-dotenv | Load HF_TOKEN from .env | `load_dotenv()` at app startup |

---

## 7. Error Handling

### 7.1 LLM Call Failures
- All calls wrapped in `try/except`
- 3 retries with 2-second sleep between each
- Non-200 HTTP status → retry
- All retries exhausted → return `"⚠️ Model failed to respond"`

### 7.2 Compliance Loop Cap
- Maximum **2 iterations** to prevent infinite rewrite loops
- If content still non-compliant after 2 rewrites → pipeline continues with best available version

### 7.3 Token Truncation
- Each agent has a tuned `max_tokens` value to prevent mid-sentence cutoffs
- Brief Agent uses 2000 (JSON is verbose); Creator/Rewriter/Localization use 3000

### 7.4 Auth Errors
- 401 → invalid token; regenerate at huggingface.co/settings/tokens
- 403 → token missing "Make calls to Inference Providers" permission (Fine-grained token required)

---

## 8. Deployment

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | Streamlit | Runs on `localhost:8501` |
| Tunnel | ngrok | Exposes port 8501 as public HTTPS URL |
| LLM Backend | Hugging Face Inference API | External API — no local GPU required |
| Auth | HF Fine-grained Token | Passed via `Authorization: Bearer` header |
| Runtime | Python 3.9+ | Runs on Colab, local machine, or any VPS |

---

## 9. File Structure

```
autocontentops/
├── app.py                      ← Streamlit UI + run_pipeline() orchestrator
├── agents/
│   ├── brief_agent.py          ← JSON plan generation
│   ├── creator_agent.py        ← Blog + LinkedIn + Twitter
│   ├── compliance_agent.py     ← Issue detection
│   ├── rewriter_agent.py       ← Content correction
│   └── localization_agent.py   ← Hinglish conversion
├── utils/
│   └── llm.py                  ← Shared call_llm() with retry logic
├── docs/
│   ├── architecture.md         ← This document
│   └── impact_model.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
