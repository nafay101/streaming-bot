import streamlit as st
from google import genai
from google.genai import types

# ---------- Page setup ----------
st.set_page_config(page_title="Gemini Flash Studio", page_icon="✨", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #F7F9FF 0%, #EEF2FF 45%, #FDF4FF 100%);
    }
    .hero {
        text-align: center;
        padding: 1.6rem 1rem 1rem 1rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #6C63FF, #EC6FD2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p { color: #6B7280; font-size: 1.05rem; }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6C63FF, #8B7CFF);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.55rem 1.4rem;
        font-weight: 600;
    }
    .stButton > button:hover { filter: brightness(1.07); color: white; }
    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #E8EAF6;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(108, 99, 255, 0.06);
    }
    textarea { border-radius: 12px !important; }
    </style>
    <div class="hero">
        <h1>✨ Gemini Flash Studio</h1>
        <p>Chat, summarize and polish your writing with Google's fast Gemini model.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    if not api_key:
        api_key = st.text_input("Gemini API key", type="password",
                                help="Get a free key at aistudio.google.com")

    model = st.selectbox("Model", ["gemini-3.8-flash", "gemini-2.5-flash-lite"])
    temperature = st.slider("Creativity", 0.0, 1.5, 0.7, 0.1)

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Your key is used only in this session and is never stored.")

if not api_key:
    st.info("👈 Add your Gemini API key in the sidebar to get started.")
    st.stop()

client = genai.Client(api_key=api_key)


def stream_reply(contents, system):
    config = types.GenerateContentConfig(system_instruction=system, temperature=temperature)
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        if chunk.text:
            yield chunk.text


# ---------- Tabs ----------
chat_tab, tools_tab = st.tabs(["💬 Chat", "🛠️ Writing Tools"])

# ----- Chat -----
with chat_tab:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        history = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["content"])],
            )
            for m in st.session_state.messages
        ]

        with st.chat_message("assistant"):
            try:
                reply = st.write_stream(
                    stream_reply(history, "You are a friendly, clear and helpful assistant.")
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ----- Writing tools -----
with tools_tab:
    task = st.selectbox(
        "What would you like to do?",
        ["Summarize", "Rewrite professionally", "Explain like I'm 12", "Fix grammar"],
    )
    prompts = {
        "Summarize": "Summarize the text in a few clear bullet points.",
        "Rewrite professionally": "Rewrite the text in a polished, professional tone. Keep the meaning.",
        "Explain like I'm 12": "Explain the text in very simple words a 12-year-old would understand.",
        "Fix grammar": "Fix spelling and grammar only. Return just the corrected text.",
    }
    text = st.text_area("Paste your text here", height=200)

    if st.button("Run ✨"):
        if not text.strip():
            st.warning("Please paste some text first.")
        else:
            with st.container(border=True):
                try:
                    st.write_stream(stream_reply(text, prompts[task]))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
