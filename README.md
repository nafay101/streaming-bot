# ✨ Gemini Flash Studio

A light, clean Streamlit app powered by Google's Gemini Flash model.

**Features**
- 💬 Streaming chat assistant with memory of the conversation
- 🛠️ Writing tools: summarize, rewrite professionally, explain simply, fix grammar
- 🎨 Light, modern interface

## Run locally

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Get a free API key at https://aistudio.google.com and paste it in the sidebar,
or create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-key-here"
```

> Never commit `secrets.toml` to GitHub.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose your repo, branch `main`, main file `app.py`.
4. Open **Advanced settings → Secrets** and add: `GEMINI_API_KEY = "your-key-here"`
5. Click **Deploy**.

## Files

| File | Purpose |
|------|---------|
| `app.py` | The Streamlit app |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Light theme settings |
