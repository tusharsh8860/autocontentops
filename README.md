# 🚀 AutoContentOps
### AI Content Team in a Box

> 5 agents. 5 minutes. Blog + LinkedIn + Twitter + compliance + Hinglish — from a single campaign brief.

A multi-agent AI pipeline that automates the full marketing content lifecycle — from raw campaign brief to compliance-checked, Hinglish-localized output — in under 5 minutes. Built with **Llama 3.1 8B**, **Streamlit**, and the **Hugging Face Inference API**.

---

## 🎯 The Problem

A typical marketing content cycle involves:
-------------------------------------------------------------------------
| Task                                 | Time (Manual)      | Cost      |
|--------------------------------------|--------------------|-----------|
| Campaign briefing & strategy         | 2 hours            | ₹3,000    |
| Content creation (blog + social)     | 3 hours            | ₹2,400    |
| Compliance review                    | 1 hour             | ₹2,000    |
| Rewriting after review               | 1.5 hours          | ₹1,200    |
| Localization (Hinglish/regional)     | 2 hours            | ₹1,200    |
| **Total**                            | **9.5 hours**      | **₹9,800**|
-------------------------------------------------------------------------
AutoContentOps reduces this to **5 minutes** and **~₹0.35 in API costs**.

---

## 🤖 How It Works

Five specialized AI agents work in sequence:

```
User Input (Campaign Brief)
        ↓
[ Brief Agent ]        →  Structured JSON marketing plan
        ↓
[ Creator Agent ]      →  Blog post + LinkedIn post + Twitter thread
        ↓
[ Compliance Agent ]   →  Checks for misleading / risky claims
        ↓ (rewrites if issues found, max 2 iterations)
[ Rewriter Agent ]     →  Fixes flagged content, preserves intent
        ↓
[ Localization Agent ] →  Hinglish version for Indian Gen Z
        ↓
Streamlit UI → 3 Tabs: Plan | Content | Hinglish
```

Each agent is a specialized prompt wrapper around **Llama 3.1 8B** via the Hugging Face novita router. No agent communicates directly with another — the `run_pipeline()` orchestrator passes outputs as strings between them, keeping the system modular and easy to debug.

---

## ✨ Features

- 🧑‍💼 **Brief Agent** — converts plain English briefs into structured JSON campaign plans
- ✍️ **Creator Agent** — generates blog post, LinkedIn post, and Twitter thread in one shot
- ⚖️ **Compliance Agent** — automatically flags misleading claims, exaggerated promises, risky financial language
- 🔁 **Rewriter Agent** — rewrites flagged content while preserving the original message
- 🌍 **Localization Agent** — converts content into natural Hinglish for Indian Gen Z audiences
- 🔄 **Retry Logic** — all LLM calls retry up to 3 times with backoff
- 📊 **Streamlit UI** — clean tabbed interface showing Plan, Content, and Hinglish output

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language Model | meta-llama/Llama-3.1-8B-Instruct (novita) |
| LLM Provider | Hugging Face Inference Router |
| Frontend | Streamlit |
| Tunneling | ngrok (pyngrok) |
| HTTP Client | Python requests |
| Runtime | Python 3.9+ |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9 or higher
- A [Hugging Face](https://huggingface.co) account
- HF token with **"Make calls to Inference Providers"** permission enabled
- (Optional) [ngrok](https://ngrok.com) account for public URL

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/autocontentops.git
cd autocontentops
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Open `.env` and add your token:

```
HF_TOKEN=hf_your_token_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 4. Run the App

```bash
streamlit run app.py --server.port 8501 --server.headless true
```

Open your browser at `http://localhost:8501`

### 5. (Optional) Expose via ngrok

```bash
ngrok config add-authtoken YOUR_NGROK_TOKEN
ngrok http 8501
```

---

## 🔑 Getting Your Hugging Face Token

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **New token**
3. Select type: **Fine-grained**
4. Enable: ✅ **Make calls to Inference Providers**
5. Enable: ✅ **Make calls to serverless Inference API**
6. Click **Generate** and copy the token

> A regular "Read" token will return a **403 error**. You must use a Fine-grained token with the above permissions.

---

## 📁 Project Structure

```
autocontentops/
│
├── README.md
├── app.py                          # Streamlit UI + pipeline orchestrator
│
├── agents/
│   ├── __init__.py
│   ├── brief_agent.py              # Brief → JSON plan
│   ├── creator_agent.py            # Blog + LinkedIn + Twitter
│   ├── compliance_agent.py         # Issue detection
│   ├── rewriter_agent.py           # Content correction
│   └── localization_agent.py       # Hinglish conversion
│
├── utils/
│   ├── __init__.py
│   └── llm.py                      # Shared call_llm() with retry logic
│
├── docs/
│   ├── architecture.md             # System architecture
│   └── impact_model.md             # Business impact analysis
│
├── assets/
│   └── demo_screenshot.png
│
├── .env.example
├── .gitignore
└── requirements.txt
```

---

## 💡 Example Input

```
Launch a new fitness app called "FitFlow" targeting Indian college students 
aged 18-24. The app offers AI-powered workout plans, diet tracking, and a 
7-day free trial. We want to grow downloads by 50% in 3 months using 
Instagram, LinkedIn, and WhatsApp.
```

### Output

**Tab 1 — Plan:** Structured JSON with audience demographics, channel strategy, budget allocation, KPIs, and timeline.

**Tab 2 — Content:** A 200-word blog post, a LinkedIn post, and a 3-tweet Twitter thread — compliance-checked and rewritten if needed.

**Tab 3 — Hinglish:** The full content package converted to natural Hinglish for Indian Gen Z audiences.

---

## 📊 Impact

| Metric | Manual | AutoContentOps | Saving |
|--------|--------|----------------|--------|
| Time per campaign | 9.5 hours | 5 minutes | 99% faster |
| Cost per campaign | ₹9,800 | ₹0.35 | 99.99% cheaper |
| Campaigns per day | 1 | 50+ | 50x throughput |
| Monthly cost (20 campaigns) | ₹1,96,000 | ₹7 | ₹1,95,993 saved |

---

## 🔧 Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Model | `meta-llama/Llama-3.1-8B-Instruct:novita` | LLM model via HF router |
| Temperature | `0.7` | Controls creativity |
| Max tokens (brief) | `2000` | JSON plan output |
| Max tokens (content) | `3000` | Blog + social content |
| Max tokens (compliance) | `1000` | Short structured response |
| Retry attempts | `3` | Per LLM call |
| Compliance iterations | `2` | Max rewrite loops |

---

## 🚧 Known Limitations

- Output quality depends on prompt clarity — more specific briefs produce better results
- Compliance agent can be overly conservative with ambitious growth targets
- No persistent storage — each session starts fresh
- Localization works best for Indian English / Hinglish; other languages not tested

---

## 🗺️ Roadmap

- [ ] Add memory so agents can reference previous campaigns
- [ ] Support additional languages (Tamil, Bengali, Telugu)
- [ ] Export output as PDF / Word document
- [ ] Add image prompt suggestions for each content piece
- [ ] Connect to social media APIs for direct publishing
- [ ] Add tone customization (formal / casual / aggressive)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👤 Author

Built by **Tushar Sharma**

- GitHub: [@tusharsh8860](https://github.com/tusharsh8860)
- LinkedIn: [@tushar-sharma-8860s2003](https://www.linkedin.com/in/tushar-sharma-8860s2003/)

---

> ⭐ If this project helped you, consider giving it a star on GitHub!