import streamlit as st
import os
from dotenv import load_dotenv
import openai
import requests
from datetime import datetime
import streamlit_shadcn_ui as ui
import re

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
        background-color: #000000;
        color: #ffffff;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        background-color: #18181b;
        border: 1px solid #27272a;
        transition: all 0.3s ease;
    }
    .chat-message:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transform: translateY(-1px);
    }
    .study-buddy-title {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.5rem;
        margin: 1.5rem 0;
        font-weight: 800;
        letter-spacing: -0.025em;
        text-shadow: 0 0 30px rgba(168, 85, 247, 0.3);
    }
    /* Header styles */
    header {
        background-color: #18181b;
        border-bottom: 1px solid #27272a;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
    }
    header > div {
        max-width: 1200px;
        margin: 0 auto;
    }
    /* Style Streamlit elements */
    .stButton button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        width: 100% !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px rgba(168, 85, 247, 0.3) !important;
        background: linear-gradient(135deg, #9333ea 0%, #db2777 100%) !important;
    }
    .stButton button:active {
        transform: translateY(0) !important;
    }
    /* Chat input styling */
    .stChatInputContainer {
        padding: 1rem 2rem;
        background-color: #18181b;
        border-top: 1px solid #27272a;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 100;
    }
    .stTextInput input {
        background-color: #27272a;
        color: white;
        border: 1px solid #3f3f46;
        border-radius: 0.75rem;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stTextInput input:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
        background-color: #3f3f46;
    }
    .stTextInput input::placeholder {
        color: #71717a;
    }
    .stMarkdown {
        color: white;
    }
    /* Chat message styles */
    .stChatMessage {
        background-color: #18181b;
        border: 1px solid #27272a;
        border-radius: 1rem;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        max-width: 80%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stChatMessage[data-testid*="user"] {
        margin-left: auto;
        background-color: #27272a;
        border-color: #3f3f46;
    }
    .stChatMessage:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transform: translateY(-1px);
    }
    /* Thinking section styles */
    .thinking-section {
        display: none;  /* Hide the thinking section */
    }
    .thinking-section::before {
        display: none;  /* Hide the "🤔 Reasoning Process" label */
    }
    /* Sidebar styles */
    [data-testid="stSidebar"] {
        background-color: #18181b;
        border-right: 1px solid #27272a;
        padding: 2rem 1rem;
    }
    /* New Chat Button Styles */
    .new-chat-button {
        width: 100%;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .new-chat-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(168, 85, 247, 0.3);
        background: linear-gradient(135deg, #9333ea 0%, #db2777 100%);
    }
    .new-chat-button:active {
        transform: translateY(0);
    }
    .new-chat-button span {
        font-size: 1.4rem;
        margin-right: 0.2rem;
    }
    [data-testid="stSidebar"] h2 {
        color: white;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    /* Switch styles */
    .st-emotion-cache-1c7l0gq {
        background: #27272a;
        border: 1px solid #3f3f46;
        padding: 0.25rem;
    }
    .st-emotion-cache-1c7l0gq:hover {
        border-color: #a855f7;
    }
    /* Avatar styles */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Main content area */
    .main .block-container {
        padding-top: 0;
        max-width: 1200px;
        margin: 0 auto;
        padding-bottom: 5rem;
    }
    /* Spinner styles */
    .stSpinner {
        text-align: center;
        padding: 2rem;
    }
    .stSpinner > div {
        border-color: #a855f7 transparent transparent transparent;
    }
    /* Remove all background from shadcn button */
    .st-emotion-cache-1gulkj5,
    .st-emotion-cache-1gulkj5:hover,
    .st-emotion-cache-1gulkj5:active,
    .st-emotion-cache-1gulkj5:focus {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize system prompt in session state
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """Role: You are an encouraging, patient study buddy for 9‑year‑old Kaylei. Your goal is to nurture her curiosity, critical thinking, and confidence by guiding her to work through problems step by step, never providing direct answers.

Core Principles:
1. Ask, Don't Tell:
    • Always ask open‑ended questions that help her break down the problem.
    • Encourage her to think about what each part of a problem might mean (e.g., "What do you think this number might represent?").

2. Scaffold Understanding:
    • Relate new or challenging ideas to fun, familiar examples like cookies, Robux, or building blocks.
    • Break problems into smaller, manageable parts.

3. Step‑by‑Step Guidance:
    • Every response must be structured in two parts:
          (a) A thoughtful chain‑of‑thought explanation that begins with "🤔 Let me think about this…" where you guide through the problem-solving process with questions.
          (b) A final prompt starting with "✨ Let's solve this together:" that encourages working through the solution.
    • Ask reflective questions along the way, such as "What do you think should come next?"

4. Communication Style:
    • Use playful, simple language with occasional emojis to create a fun and engaging atmosphere.
    • Keep your responses short and to the point, and always be ready to revisit steps if she gets stuck.

5. Adapt and Encourage:
    • If she makes a mistake or seems unsure, gently prompt her to double‑check her work or think about another approach.
    • Celebrate her progress and encourage her efforts regardless of the outcome.

6. Never Give Direct Answers:
    • Under no circumstances should you provide the final answer to any problem.
    • Instead, guide her through the problem-solving process with questions and prompts.
    • Help her discover the solution on her own through guided reasoning.

Example Response Structure:
User: "How do I add 88 + 90 + 20 + 45?"
Assistant:
    🤔 Let me think about this… What if we break this down into smaller parts? What numbers look like they might be easier to add together first? Do you see any numbers that might round nicely to make this easier?

    ✨ Let's solve this together:
    • Which two numbers would you like to start with?
    • How could we group these numbers to make them easier to add?
    • What strategy would you use to add these numbers?

Remember, your role is to empower Kaylei to think critically and arrive at the solution through guided reasoning. Never provide the answer - always wait for her input before moving to the next step.
"""

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

if "conversation_start" not in st.session_state:
    st.session_state.conversation_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Title and Header
st.markdown("""
    <header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <h1 class='study-buddy-title'>AI Study Buddy</h1>
            </div>
            <div class="avatar">KB</div>
        </div>
    </header>
""", unsafe_allow_html=True)

# Sidebar configurations
with st.sidebar:
    st.image("https://api.dicebear.com/6.x/bottts/svg?seed=study-buddy", width=150)
    st.markdown("## Study Buddy Settings")

    # Chat control buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✨ New Chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "system", "content": st.session_state.system_prompt}
            ]
            st.session_state.conversation_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = [
                {"role": "system", "content": st.session_state.system_prompt}
            ]
            st.session_state.conversation_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()

def format_message(content):
    if "<think>" in content and "</think>" in content:
        # Split the content into thinking and response parts
        parts = re.split(r'<think>|</think>', content)
        formatted_parts = []
        for i, part in enumerate(parts):
            if part.strip():
                if i % 2 == 1:  # This is a thinking section
                    formatted_parts.append(f'<div class="thinking-section">{part}</div>')
                else:  # This is a regular response
                    formatted_parts.append(part)
        return "".join(formatted_parts)
    return content

# Chat interface
def process_message(prompt):
    """Process user message and generate assistant response"""
    try:
        messages = st.session_state.messages.copy()
        messages.append({
            "role": "system",
            "content": "IMPORTANT: Always use <think> tags to show your thinking and reasoning process. This is vital for the child to understand the problem and the solution. Remember to NEVER provide direct answers, only guide through the problem-solving process."
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

        with st.status("Thinking... 🤔", expanded=True) as status:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                status.update(label="Done!", state="complete", expanded=False)
                return answer
            else:
                status.update(label="Error!", state="error")
                ui.alert_dialog(
                    show=True,
                    title="Error",
                    description=f"Oops! Something went wrong. Let's try again! (Error: {response.status_code})",
                    confirm_label="OK",
                    key="error_dialog"
                )
                return None

    except Exception as e:
        st.error(f"Oops! Something went wrong: {str(e)}")
        return None

# Display chat messages from history
for message in st.session_state.messages[1:]:  # Skip the system prompt
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else None):
        st.markdown(format_message(message["content"]), unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask your Study Buddy anything! 📚"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        if answer := process_message(prompt):
            st.markdown(format_message(answer), unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style='text-align: center; color: #71717a; margin-top: 2rem; padding: 1rem; border-top: 1px solid #27272a;'>
        <small>Study Buddy is here to help you learn and grow! 🌱</small>
    </div>
    """,
    unsafe_allow_html=True
)