# 🧠 The Memory Vault — Stateful Chatbot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Stateful%20Chat-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-API-8E75B2?style=for-the-badge&logo=google)
![Status](https://img.shields.io/badge/Assignment%203-Completed-success?style=for-the-badge)

### A Gemini-powered Streamlit chatbot that remembers the conversation using `st.session_state`.

</div>

---

## 📌 Video Demo

https://github.com/user-attachments/assets/307e4451-a117-4709-875c-cd6bc3628a6a

---

## 🎯 Objective

Earlier versions of the chatbot were stateless. Every time Streamlit reran the script, the app could lose its previous conversation.

This upgraded version uses Streamlit's **Memory Vault**:

```python
st.session_state
```

This allows the chatbot to remember messages across reruns, including when the sidebar personality dropdown or intensity slider changes.

---

## ✅ Core Requirements Completed

| Task | Requirement | Status |
|---|---|---|
| Task 1 | Initialize `st.session_state.messages` | ✅ Done |
| Task 2 | Render previous chat history using a loop | ✅ Done |
| Task 3 | Replace old input/button with `st.chat_input()` | ✅ Done |
| Task 3 | Use walrus operator `:=` | ✅ Done |
| Task 4 | Save user message to memory | ✅ Done |
| Task 4 | Save Gemini response to memory | ✅ Done |
| Extra | Sidebar personality dropdown retained | ✅ Done |
| Extra | Intensity slider retained | ✅ Done |
| Extra | Dynamic avatars retained | ✅ Done |
| Extra | Clear memory button added | ✅ Done |

---

## 🧠 How Memory Works

The app starts by checking whether `messages` already exists:

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

Every user and assistant message is stored as a dictionary:

```python
{"role": "user", "content": user_message}
{"role": "assistant", "content": response.text}
```

Then, on every rerun, the app redraws all messages:

```python
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

---

## ✨ Features

- Gemini-powered chatbot
- Stateful conversation memory
- Native Streamlit chat UI
- `st.chat_input()` instead of old text input + button
- Sidebar personality selector
- Sidebar intensity slider
- Dynamic bot avatars
- Clear Memory Vault button
- Modern styled interface
- Conversation context passed back to Gemini

---

## 🎭 Available Personalities

- 🌸 A friendly AI mentor
- 💻 An expert Hacker
- 🚀 A wise space explorer
- 😵‍💫 A panicked college student at 3 AM
- 🎩 A 1920s Mafia Boss
- 🏋️ A highly sarcastic fitness coach
- 🤖 A dramatic Shakespearean robot
- 🧸 A cheerful kindergarten teacher

---

## 🔐 Gemini API Key Setup

The app reads your Gemini API key from either:

1. Streamlit secrets
2. Environment variable

### Option 1: Streamlit Secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### Option 2: Environment Variable

#### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

#### macOS/Linux

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

---

## 🚀 How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Streamlit

```bash
streamlit run app.py
```

### 3. Open the local URL

```text
http://localhost:8501
```

---

## 🧪 Testing Checklist

Before submitting, test this exact flow:

1. Open the local app.
2. Send message 1.
3. Send message 2.
4. Send message 3.
5. Confirm message 1 is still visible.
6. Change the personality dropdown.
7. Confirm previous messages still remain on screen.
8. Move the intensity slider.
9. Confirm previous messages still remain on screen.
10. Record the screen.

---

## 📁 Project Structure

```text
memory-vault-stateful-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

<div align="center">

### Built with 💙 using Streamlit + Gemini + Session State

</div>
