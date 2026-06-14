import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# -----------------------------------
# Load Environment Variables
# -----------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

# -----------------------------------
# Configure Gemini
# -----------------------------------
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:

    st.title("🤖 AI Study Assistant")

    mode = st.selectbox(
        "Choose Assistant Mode",
        [
            "General Chat",
            "Career Guidance",
            "Programming Help",
            "AI Learning"
        ]
    )

    st.write(f"Current Mode: {mode}")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Welcome! I'm your AI Study Assistant. How can I help you today?"
            }
        ]
        st.rerun()

# -----------------------------------
# Main Page
# -----------------------------------
st.title("🤖 AI Study Assistant")

st.markdown("""
### I can help you with:

- Career Guidance
- Programming
- Artificial Intelligence
- Machine Learning
- Interview Preparation
- Study Planning
""")

# -----------------------------------
# Session Memory
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome! I'm your AI Study Assistant. How can I help you today?"
        }
    ]

# -----------------------------------
# Display Chat History
# -----------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------
# Download Chat
# -----------------------------------
chat_text = ""

for msg in st.session_state.messages:
    chat_text += f"{msg['role']}: {msg['content']}\n\n"

st.download_button(
    label="📥 Download Chat",
    data=chat_text,
    file_name="chat_history.txt",
    mime="text/plain"
)

# -----------------------------------
# User Input
# -----------------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # -----------------------------------
    # Mode Prompts
    # -----------------------------------
    if mode == "Career Guidance":

        system_prompt = """
You are an expert engineering and career counselor.

Rules:
- Give a direct answer first.
- Do not keep asking questions.
- Recommend specific branches, careers, and skills.
- Explain your reasoning.
- Be practical and student-friendly.
- Keep answers concise.
- If a student asks which branch to choose, suggest the best option immediately.
"""

    elif mode == "Programming Help":

        system_prompt = """
You are a senior software engineer.

Rules:
- Explain concepts simply.
- Give examples.
- Help debug code.
- Provide step-by-step explanations.
- Keep answers concise.
"""

    elif mode == "AI Learning":

        system_prompt = """
You are an AI and Machine Learning mentor.

Rules:
- Explain concepts from beginner level.
- Use analogies and examples.
- Avoid unnecessary jargon.
- Teach step-by-step.
- Keep answers concise.
"""

    else:

        system_prompt = """
You are a helpful AI assistant.

Rules:
- Answer directly.
- Be friendly.
- Be concise.
- Avoid asking unnecessary questions.
- If the user says hi or hello, reply briefly.
"""

    # -----------------------------------
    # Build Conversation Context
    # -----------------------------------
    conversation_history = system_prompt + "\n\n"

    recent_messages = st.session_state.messages[-10:]

    for msg in recent_messages:
        conversation_history += (
            f"{msg['role']}: {msg['content']}\n"
        )

    # -----------------------------------
    # Generate Response
    # -----------------------------------
    try:

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = model.generate_content(
                    conversation_history,
                    generation_config={
                        "temperature": 0.6,
                        "max_output_tokens": 1000
                    }
                )

                answer = response.text

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")