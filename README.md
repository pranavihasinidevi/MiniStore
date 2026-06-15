# 🛍️ MiniStore v3 — AI-Powered E-Commerce + OpenAI Chatbot

## 📁 Complete Folder Structure

```
MiniStore/
├── app.py                          ← Homepage (products, cart, categories)
├── requirements.txt                ← Dependencies
├── .gitignore                      ← Protects secrets from Git
├── README.md                       ← This file
├── .streamlit/
│   └── secrets.toml                ← Your OpenAI API key (NEVER commit)
└── pages/
    └── 1_Support_Chatbot.py        ← AI chatbot page (plain ASCII filename!)
```

## ⚠️ IMPORTANT: Filename Rules

The chatbot page MUST be named exactly:
```
1_Support_Chatbot.py
```
- ✅ Use underscores, not spaces
- ✅ Plain ASCII only — NO emoji in the actual filename
- ✅ Must be inside the `pages/` folder
- ✅ Streamlit will show it as "1 Support Chatbot" in the sidebar nav

## 🔑 Step 1 — Get your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create a free account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)

## 🔐 Step 2 — Add your API Key

Create the file `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
```

## 📦 Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit>=1.32.0`
- `openai>=1.30.0`

## 🚀 Step 4 — Run the App

```bash
streamlit run app.py
```

## 🤖 How the Chatbot Works

| Feature | Detail |
|---------|--------|
| Model | GPT-4o Mini (fast + affordable) |
| API key | Read from `st.secrets["OPENAI_API_KEY"]` |
| System prompt | Includes full product catalogue + store policies |
| Scope | Restricted to store topics only — off-topic redirected |
| History | Stored in `st.session_state.chat_history` |
| Temperature | 0.4 (factual but natural) |
| Max tokens | 600 per response |

## 💰 OpenAI Cost Estimate

GPT-4o Mini pricing (as of 2025):
- Input:  ~$0.15 per 1M tokens
- Output: ~$0.60 per 1M tokens
- Typical support chat: ~500–1000 tokens per exchange
- **Estimated cost: < $0.01 per conversation**

## 🔒 Security Checklist

- [x] `secrets.toml` added to `.gitignore`
- [x] API key never hardcoded in Python files
- [x] API key read only via `st.secrets["OPENAI_API_KEY"]`
- [ ] Rotate your key if accidentally pushed to GitHub
