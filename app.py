import os
import streamlit as st
import google.generativeai as genai


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="The Memory Vault",
    page_icon="🧠",
    layout="centered",
)


# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(34, 211, 238, 0.22), transparent 32%),
            radial-gradient(circle at bottom right, rgba(168, 85, 247, 0.20), transparent 35%),
            linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.18);
    }

    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.25rem;
        background: linear-gradient(90deg, #67e8f9, #a78bfa, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-text {
        text-align: center;
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    .memory-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
        margin-bottom: 1rem;
    }

    .settings-pill {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #bae6fd;
        font-size: 0.85rem;
        margin-right: 0.35rem;
        margin-top: 0.35rem;
    }

    .footer-note {
        color: #94a3b8;
        text-align: center;
        font-size: 0.82rem;
        margin-top: 1.5rem;
    }

    div[data-testid="stChatInput"] {
        border-radius: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Gemini API Setup
# ---------------------------------------------------------
def get_api_key() -> str | None:
    """
    Reads the Gemini API key from Streamlit secrets first,
    then from the system environment variable.
    """
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


api_key = get_api_key()

if api_key:
    genai.configure(api_key=api_key)


# ---------------------------------------------------------
# Task 1: Initialize the Memory Vault
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Sidebar Settings
# ---------------------------------------------------------
st.sidebar.title("App Settings")

personalities = [
    "A friendly AI mentor",
    "An expert Hacker",
    "A wise space explorer",
    "A panicked college student at 3 AM",
    "A 1920s Mafia Boss",
    "A highly sarcastic fitness coach",
    "A dramatic Shakespearean robot",
    "A cheerful kindergarten teacher",
]

selected_personality = st.sidebar.selectbox(
    "Choose AI Personality",
    personalities,
)

intensity_level = st.sidebar.slider(
    "Intensity Level",
    min_value=1,
    max_value=10,
    value=6,
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "The Memory Vault uses st.session_state, so changing these settings will not erase your chat history."
)

if st.sidebar.button("Clear Memory Vault"):
    st.session_state.messages = []
    st.rerun()


# ---------------------------------------------------------
# Dynamic Avatars
# ---------------------------------------------------------
if selected_personality == "A friendly AI mentor":
    bot_avatar = "🌸"
elif selected_personality == "An expert Hacker":
    bot_avatar = "💻"
elif selected_personality == "A wise space explorer":
    bot_avatar = "🚀"
elif selected_personality == "A panicked college student at 3 AM":
    bot_avatar = "😵‍💫"
elif selected_personality == "A 1920s Mafia Boss":
    bot_avatar = "🎩"
elif selected_personality == "A highly sarcastic fitness coach":
    bot_avatar = "🏋️"
elif selected_personality == "A dramatic Shakespearean robot":
    bot_avatar = "🤖"
elif selected_personality == "A cheerful kindergarten teacher":
    bot_avatar = "🧸"
else:
    bot_avatar = "✨"


# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------
st.markdown('<h1 class="main-title">🧠 The Memory Vault</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-text">A stateful Gemini chatbot that remembers your full conversation using Streamlit session state.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="memory-card">
        <strong>Current Vault Settings</strong><br>
        <span class="settings-pill">Persona: {selected_personality}</span>
        <span class="settings-pill">Intensity: {intensity_level}/10</span>
        <span class="settings-pill">Bot Avatar: {bot_avatar}</span>
        <span class="settings-pill">Saved Messages: {len(st.session_state.messages)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Prompt Engineering
# ---------------------------------------------------------
ai_instructions = f"""
You are acting as: {selected_personality}.

Your personality intensity level is {intensity_level} out of 10.

Follow these rules:
- Stay in the selected personality throughout the response.
- If intensity is 1 to 3, keep the personality subtle and mostly professional.
- If intensity is 4 to 7, make the personality clearly noticeable and entertaining.
- If intensity is 8 to 10, act very strongly in character while still being useful and understandable.
- Remember the conversation history provided by the app.
- Answer the user's latest message clearly and naturally.
- Keep responses concise, helpful, and engaging.
"""


# ---------------------------------------------------------
# Task 2: Render the Chat History
# ---------------------------------------------------------
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar=message.get("avatar", bot_avatar)):
            st.markdown(message["content"])


# ---------------------------------------------------------
# Task 3: Upgrade the Input UI with st.chat_input
# ---------------------------------------------------------
if user_message := st.chat_input("Say something..."):
    if not api_key:
        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY in Streamlit secrets "
            "or set it as an environment variable."
        )
    else:
        # -------------------------------------------------
        # Task 4: Save New User Message to Memory
        # -------------------------------------------------
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_message)

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=ai_instructions,
            )

            # Send previous conversation history as context.
            conversation_context = ""
            for message in st.session_state.messages:
                conversation_context += f'{message["role"].upper()}: {message["content"]}\n'

            prompt = f"""
Conversation so far:
{conversation_context}

Respond to the latest USER message while respecting the full conversation context.
"""

            with st.spinner("Unlocking the Memory Vault..."):
                response = model.generate_content(prompt)

            assistant_reply = (
                response.text
                if response and response.text
                else "I could not generate a response. Please try again."
            )

            # -------------------------------------------------
            # Task 4: Save Gemini Response to Memory
            # -------------------------------------------------
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply,
                    "avatar": bot_avatar,
                }
            )

            with st.chat_message("assistant", avatar=bot_avatar):
                st.markdown(assistant_reply)

        except Exception as error:
            st.error(f"Something went wrong while contacting Gemini: {error}")


st.markdown(
    '<p class="footer-note">Built for MirAI School of Technology — AI Builder Track Assignment 3</p>',
    unsafe_allow_html=True,
)
