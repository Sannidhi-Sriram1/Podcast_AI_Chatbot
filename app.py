import streamlit as st
import requests

# --------------- Hugging Face Settings ---------------
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_TOKEN = ""  # Replace with your token

headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.json()


# --------------- Page Config ---------------
st.set_page_config(
    page_title="Podcast Playlist AI",
    page_icon="🎧",
    layout="wide"
)

# --------------- Session State Init ---------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"  # Default light mode

# --------------- Sidebar (Chat History + Theme + Clear History) ---------------
with st.sidebar:
    st.title("🗂️ Chat History")

    # Display the chat history (latest 10 chats)
    if st.session_state.chat_history:
        for idx, chat in enumerate(reversed(st.session_state.chat_history[-10:])):
            with st.expander(f"💬 {chat['prompt'][:30]}..."):
                st.markdown(f"**Prompt:** {chat['prompt']}")
                st.markdown(f"**AI Playlist:**\n\n```\n{chat['response']}\n```")
    else:
        st.info("No chats yet. Start creating!")

    st.markdown("---")

    # **Clear History Button**
    clear_history = st.button("❌ Clear History")
    if clear_history:
        st.session_state.chat_history.clear()
        st.success("🧹 History cleared!")

    st.markdown("---")

    # **Theme Toggle**
    theme_toggle = st.radio("🌗 Select Theme", ["Light", "Dark"],
                            index=0 if st.session_state.theme_mode == "light" else 1)
    st.session_state.theme_mode = theme_toggle.lower()

    st.markdown("---")
    st.caption("Made by Sriram")

# --------------- Main Panel ---------------
st.title("🎧 AI-Powered Podcast Playlist Generator")
st.markdown("Craft a personalized podcast playlist tailored to your passions using AI!")

user_input = st.text_area("What are you into? 📝", "Startups, AI, Wellness, Storytelling")
generate = st.button("🔍 Generate Playlist")

if generate:
    with st.spinner("Generating playlist..."):
        prompt = (
            f"Create a list of 5 engaging podcast episodes based on: {user_input}. "
            "For each, include:\n1. Podcast title\n2. Short description\n3. Genre/category.\n"
            "Keep it fun, informative, and tailored to interests."
        )
        response = query(prompt)

        if isinstance(response, dict) and "error" in response:
            st.error(f"❌ API Error: {response['error']}")
        else:
            result = response[0]['generated_text']
            st.session_state.chat_history.append({"prompt": user_input, "response": result})
            st.success("✅ Playlist Ready!")
            st.markdown(f"```markdown\n{result}\n```")

# --------------- Custom Theme Styling (CSS for Light/Dark Mode) ---------------

custom_dark_css = """
<style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stTextArea textarea {
        background-color: #262730;
        color: white;
    }
    .stButton > button {
        background-color: #555555;
        color: white;
    }
</style>
"""

custom_light_css = """
<style>
    body {
        background-color: #f7f7f7;
        color: black;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        color: black;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
    }
</style>
"""

# Toggle theme based on selection
if st.session_state.theme_mode == "dark":
    st.markdown(custom_dark_css, unsafe_allow_html=True)
else:
    st.markdown(custom_light_css, unsafe_allow_html=True)
