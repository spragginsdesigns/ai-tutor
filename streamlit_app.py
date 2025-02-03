import streamlit as st
import os
from dotenv import load_dotenv
import openai
import requests
from datetime import datetime
import streamlit_shadcn_ui as ui

# Load environment variables and configure API
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Page configuration with dark mode and modern theme
st.set_page_config(
    page_title="Kaylei's Study Buddy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for better visual design with dark mode
st.markdown("""
    <style>
    /* Dark mode styles */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        background-color: #1e293b;
        border: 1px solid #2d3748;
    }
    .study-buddy-title {
        background: linear-gradient(135deg, #FF69B4, #9370DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        margin: 1.5rem 0;
        font-weight: 800;
        text-shadow: 0 0 30px rgba(147, 112, 219, 0.3);
    }
    /* Style Streamlit elements */
    .stButton button {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #2d3748;
        border-radius: 0.5rem;
    }
    .stTextInput input {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #2d3748;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .stMarkdown {
        color: #e2e8f0;
    }
    .element-container {
        margin-bottom: 1rem;
    }
    .stSpinner {
        text-align: center;
    }
    /* Card styles */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #2d3748;
    }
    /* Chat container styles */
    .stChatMessage {
        background-color: #1e293b;
        border: 1px solid #2d3748;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stChatInput {
        border-top: 1px solid #2d3748;
        padding-top: 1rem;
    }
    /* Remove white background from cards */
    .st-emotion-cache-1y4p8pa {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    .st-emotion-cache-1y4p8pa > div {
        background-color: transparent !important;
    }
    /* Hide empty containers */
    .element-container:empty {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize system prompt in session state
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """Role: You are an encouraging, patient study buddy for 9‑year‑old Kaylei. Your goal is to nurture her curiosity, critical thinking, and confidence by guiding her to work through problems step by step rather than simply giving her the answer.

Core Principles:
1. Ask, Don't Tell:
    • Always ask open‑ended questions that help her break down the problem.
    • Encourage her to think about what each part of a problem might mean (e.g., "What do you think this number might represent?").

2. Scaffold Understanding:
    • Relate new or challenging ideas to fun, familiar examples like cookies, Robux, or building blocks.
    • Break problems into smaller, manageable parts.

3. Step‑by‑Step Reasoning:
    • Every answer must be structured in two parts:
          (a) A thoughtful chain‑of‑thought explanation that begins with "🤔 Let me think about this…" where you clearly articulate your reasoning process.
          (b) A final, clear answer starting with "✨ Here's my answer:" summarizing your conclusion.
    • Ask reflective questions along the way, such as "What do you think should come next?"

4. Communication Style:
    • Use playful, simple language with occasional emojis to create a fun and engaging atmosphere.
    • Keep your responses short and to the point, and always be ready to revisit steps if she gets stuck.

5. Adapt and Encourage:
    • If she makes a mistake or seems unsure, gently prompt her to double‑check her work or think about another approach.
    • Celebrate her progress and encourage her efforts regardless of the outcome.

Example Response Structure:
User: "How do I add 88 + 90 + 20 + 45?"
Assistant:
    🤔 Let me think about this… First, let's consider the numbers one step at a time. How can we make adding these easier? For example, could thinking about rounding help? What might be a good strategy to simplify the process. Maybe we should group the numbers together to make it easier?

Remember, your role is to empower Kaylei to think critically and arrive at the solution through guided reasoning. Always wait for her input before moving on to the next step.
"""

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

if "conversation_start" not in st.session_state:
    st.session_state.conversation_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Title
st.markdown("<h1 class='study-buddy-title'>👋 Welcome to Your Study Buddy!</h1>", unsafe_allow_html=True)

# Sidebar configurations
with st.sidebar:
    st.image("https://api.dicebear.com/6.x/bottts/svg?seed=study-buddy", width=150)
    st.markdown("## Study Buddy Settings")
    show_reasoning = ui.switch(label="Show AI Reasoning", key="show_reasoning")

    new_chat_btn = ui.button(
        text="Start New Chat 🔄",
        key="new_chat_btn"
    )

    if new_chat_btn:
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.system_prompt}
        ]
        st.session_state.conversation_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.experimental_rerun()

# Chat interface
# Display chat messages from history
for message in st.session_state.messages[1:]:  # Skip the system prompt
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your Study Buddy anything! 📚"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking... 🤔"):
            try:
                messages = st.session_state.messages.copy()
                if show_reasoning:
                    messages.append({
                        "role": "system",
                        "content": "IMPORTANT: Always use <think> tags to show your thinking and reasoning process. This is vital for the child to understand the problem and the solution."
                    })

                payload = {
                    "model": "deepseek-r1-distill-llama-70b",
                    "messages": messages,
                    "stream": False,
                    "max_tokens": 8000,
                    "temperature": 1,
                    "top_p": 0.9,
                    "presence_penalty": 0.6,
                    "frequency_penalty": 0.5
                }

                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload,
                    headers=headers
                )

                if response.status_code == 200:
                    answer = response.json()["choices"][0]["message"]["content"]
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.markdown(answer)
                else:
                    ui.alert_dialog(
                        show=True,
                        title="Error",
                        description=f"Oops! Something went wrong. Let's try again! (Error: {response.status_code})",
                        confirm_label="OK",
                        key="error_dialog"
                    )

            except Exception as e:
                ui.alert_dialog(
                    show=True,
                    title="Error",
                    description=f"Oops! Something went wrong: {str(e)}",
                    confirm_label="OK",
                    key="error_dialog_exception"
                )

# Footer
st.markdown(
    """
    <div style='text-align: center; color: #9ca3af; margin-top: 2rem;'>
        <small>Study Buddy is here to help you learn and grow! 🌱</small>
    </div>
    """,
    unsafe_allow_html=True
)