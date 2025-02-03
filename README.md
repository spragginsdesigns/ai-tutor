# 👋 AI Tutor Study Buddy

*Welcome to AI Tutor Study Buddy – your interactive, friendly assistant designed to help learners build confidence and critical thinking skills!*

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Technology Stack](#technology-stack)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

AI Tutor Study Buddy is an engaging and interactive educational app built with [Streamlit](https://streamlit.io/). The app is designed as a chat interface where the assistant provides guided, step-by-step help for problem-solving, making learning both fun and effective.

The assistant’s personality is carefully crafted to encourage learners to think critically by asking open-ended questions, scaffolding complex topics with relatable examples, and celebrating each learning milestone. All of this is presented with a sleek, modern, and dark-themed UI!

---

## Features

- **Interactive Chat Interface:**  
  Enjoy a real-time conversation with your AI Tutor.

- **Step-by-Step Reasoning:**  
  Every answer is structured in two parts: a chain-of-thought explanation and a clear final answer.

- **Customizable UI:**  
  Enjoy a beautifully designed dark mode theme with smooth animations and modern CSS.

- **Dynamic Environment:**  
  Uses external APIs and environment configurations (via `.env`) to deliver a responsive experience.

- **Reset and New Chat:**  
  Easily start fresh conversations with a single click.

- **AI Reasoning Toggle:**  
  Option to show or hide detailed AI reasoning for enhanced educational insights.

---

## Setup & Installation

### Prerequisites

- **Python 3.9+**  
- **Pip** (Python package installer)

### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ai-tutor-study-buddy.git
   cd ai-tutor-study-buddy
   ```

2. **Create a Virtual Environment (Optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables:**

   Create a `.env` file in the root directory and add your API key:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

---

## Configuration

This app leverages several external libraries:
- **Streamlit:** For the web interface.
- **python-dotenv:** To load environment variables.
- **Requests:** For making API calls.
- **streamlit_shadcn_ui:** For modern UI components.

All configurations such as page title, dark mode theme, and sidebar settings are defined in the main script. You can further customize these settings by modifying the corresponding sections in the code.

---

## Usage

1. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the Chat Interface:**

   - **Chat:** Ask your AI Tutor any question or request assistance with a problem.
   - **New Chat:** Start a fresh conversation using the "Start New Chat 🔄" button in the sidebar.
   - **Toggle AI Reasoning:** Use the switch in the sidebar to show or hide detailed reasoning.

3. **Enjoy Learning:**

   Watch as the AI Tutor uses a playful and step-by-step approach to help guide you through your questions!

---

## Technology Stack

- **Python** – The backbone of our application.
- **Streamlit** – Rapidly build and deploy interactive web apps.
- **OpenAI API (via GROQ)** – Powers the natural language responses.
- **Custom CSS** – Enhances the dark mode and overall design.
- **Streamlit Shadcn UI** – Provides additional modern UI components.

---

## Customization

- **UI Styling:**  
  Modify the embedded CSS in `app.py` to change the look and feel of your app.

- **System Prompt:**  
  The assistant’s behavior and response style can be adjusted by editing the system prompt in the session state initialization section.

- **API Integration:**  
  Update the API endpoints and request parameters as needed to fit your integration requirements.

---

## Troubleshooting

- **API Errors:**  
  If you encounter issues with API responses, check that your `GROQ_API_KEY` is correctly set in your `.env` file and that the API endpoint is accessible.

- **Streamlit Issues:**  
  Make sure all dependencies are installed correctly. Use `pip freeze` to verify package versions.

- **General Debugging:**  
  Utilize Streamlit’s in-built error messages and logs to troubleshoot issues.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Happy learning! Let AI Tutor Study Buddy help you unlock your potential, one question at a time.*  

---

*Note: This project demonstrates how engaging, interactive educational tools can be built using modern web technologies and AI-driven responses.*
