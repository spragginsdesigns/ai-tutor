Build a basic LLM chat app
Introduction

The advent of large language models like GPT has revolutionized the ease of developing chat-based applications. Streamlit offers several Chat elements, enabling you to build Graphical User Interfaces (GUIs) for conversational agents or chatbots. Leveraging session state along with these elements allows you to construct anything from a basic chatbot to a more advanced, ChatGPT-like experience using purely Python code.

In this tutorial, we'll start by walking through Streamlit's chat elements, st.chat_message and st.chat_input. Then we'll proceed to construct three distinct applications, each showcasing an increasing level of complexity and functionality:

    First, we'll Build a bot that mirrors your input to get a feel for the chat elements and how they work. We'll also introduce session state and how it can be used to store the chat history. This section will serve as a foundation for the rest of the tutorial.
    Next, you'll learn how to Build a simple chatbot GUI with streaming.
    Finally, we'll Build a ChatGPT-like app that leverages session state to remember conversational context, all within less than 50 lines of code.

Here's a sneak peek of the LLM-powered chatbot GUI with streaming we'll build in this tutorial:
Built with Streamlit 🎈
Fullscreen
open_in_new

Play around with the above demo to get a feel for what we'll build in this tutorial. A few things to note:

    There's a chat input at the bottom of the screen that's always visible. It contains some placeholder text. You can type in a message and press Enter or click the run button to send it.
    When you enter a message, it appears as a chat message in the container above. The container is scrollable, so you can scroll up to see previous messages. A default avatar is displayed to your messages' left.
    The assistant's responses are streamed to the frontend and are displayed with a different default avatar.

Before we start building, let's take a closer look at the chat elements we'll use.
Chat elements

Streamlit offers several commands to help you build conversational apps. These chat elements are designed to be used in conjunction with each other, but you can also use them separately.

st.chat_message lets you insert a chat message container into the app so you can display messages from the user or the app. Chat containers can contain other Streamlit elements, including charts, tables, text, and more. st.chat_input lets you display a chat input widget so the user can type in a message.

For an overview of the API, check out this video tutorial by Chanin Nantasenamat (@dataprofessor), a Senior Developer Advocate at Streamlit.
st.chat_message

st.chat_message lets you insert a multi-element chat message container into your app. The returned container can contain any Streamlit element, including charts, tables, text, and more. To add elements to the returned container, you can use with notation.

st.chat_message's first parameter is the name of the message author, which can be either "user" or "assistant" to enable preset styling and avatars, like in the demo above. You can also pass in a custom string to use as the author name. Currently, the name is not shown in the UI but is only set as an accessibility label. For accessibility reasons, you should not use an empty string.

Here's an minimal example of how to use st.chat_message to display a welcome message:
import streamlit as st

with st.chat_message("user"):
    st.write("Hello 👋")

Notice the message is displayed with a default avatar and styling since we passed in "user" as the author name. You can also pass in "assistant" as the author name to use a different default avatar and styling, or pass in a custom name and avatar. See the API reference for more details.
import streamlit as st
import numpy as np

with st.chat_message("assistant"):
    st.write("Hello human")
    st.bar_chart(np.random.randn(30, 3))
Built with Streamlit 🎈
Fullscreen
open_in_new

While we've used the preferred with notation in the above examples, you can also just call methods directly in the returned objects. The below example is equivalent to the one above:
import streamlit as st
import numpy as np

message = st.chat_message("assistant")
message.write("Hello human")
message.bar_chart(np.random.randn(30, 3))

So far, we've displayed predefined messages. But what if we want to display messages based on user input?
st.chat_input

st.chat_input lets you display a chat input widget so the user can type in a message. The returned value is the user's input, which is None if the user hasn't sent a message yet. You can also pass in a default prompt to display in the input widget. Here's an example of how to use st.chat_input to display a chat input widget and show the user's input:
import streamlit as st

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
Built with Streamlit 🎈
Fullscreen
open_in_new

Pretty straightforward, right? Now let's combine st.chat_message and st.chat_input to build a bot the mirrors or echoes your input.
Build a bot that mirrors your input

In this section, we'll build a bot that mirrors or echoes your input. More specifically, the bot will respond to your input with the same message. We'll use st.chat_message to display the user's input and st.chat_input to accept user input. We'll also use session state to store the chat history so we can display it in the chat message container.

First, let's think about the different components we'll need to build our bot:

    Two chat message containers to display messages from the user and the bot, respectively.
    A chat input widget so the user can type in a message.
    A way to store the chat history so we can display it in the chat message containers. We can use a list to store the messages, and append to it every time the user or bot sends a message. Each entry in the list will be a dictionary with the following keys: role (the author of the message), and content (the message content).

import streamlit as st

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

In the above snippet, we've added a title to our app and a for loop to iterate through the chat history and display each message in the chat message container (with the author role and message content). We've also added a check to see if the messages key is in st.session_state. If it's not, we initialize it to an empty list. This is because we'll be adding messages to the list later on, and we don't want to overwrite the list every time the app reruns.

Now let's accept user input with st.chat_input, display the user's message in the chat message container, and add it to the chat history.
# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

We used the := operator to assign the user's input to the prompt variable and checked if it's not None in the same line. If the user has sent a message, we display the message in the chat message container and append it to the chat history.

All that's left to do is add the chatbot's responses within the if block. We'll use the same logic as before to display the bot's response (which is just the user's prompt) in the chat message container and add it to the history.
response = f"Echo: {prompt}"
# Display assistant response in chat message container
with st.chat_message("assistant"):
    st.markdown(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})

Putting it all together, here's the full code for our simple chatbot GUI and the result:
View full code
expand_more
Built with Streamlit 🎈
Fullscreen
open_in_new

While the above example is very simple, it's a good starting point for building more complex conversational apps. Notice how the bot responds instantly to your input. In the next section, we'll add a delay to simulate the bot "thinking" before responding.
Build a simple chatbot GUI with streaming

In this section, we'll build a simple chatbot GUI that responds to user input with a random message from a list of pre-determind responses. In the next section, we'll convert this simple toy example into a ChatGPT-like experience using OpenAI.

Just like previously, we still require the same components to build our chatbot. Two chat message containers to display messages from the user and the bot, respectively. A chat input widget so the user can type in a message. And a way to store the chat history so we can display it in the chat message containers.

Let's just copy the code from the previous section and add a few tweaks to it.
import streamlit as st
import random
import time

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

The only difference so far is we've changed the title of our app and added imports for random and time. We'll use random to randomly select a response from a list of responses and time to add a delay to simulate the chatbot "thinking" before responding.

All that's left to do is add the chatbot's responses within the if block. We'll use a list of responses and randomly select one to display. We'll also add a delay to simulate the chatbot "thinking" before responding (or stream its response). Let's make a helper function for this and insert it at the top of our app.
# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

Back to writing the response in our chat interface, we'll use st.write_stream to write out the streamed response with a typewriter effect.
# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator())
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})

Above, we've added a placeholder to display the chatbot's response. We've also added a for loop to iterate through the response and display it one word at a time. We've added a delay of 0.05 seconds between each word to simulate the chatbot "thinking" before responding. Finally, we append the chatbot's response to the chat history. As you've probably guessed, this is a naive implementation of streaming. We'll see how to implement streaming with OpenAI in the next section.

Putting it all together, here's the full code for our simple chatbot GUI and the result:
View full code
expand_more
Built with Streamlit 🎈
Fullscreen
open_in_new

Play around with the above demo to get a feel for what we've built. It's a very simple chatbot GUI, but it has all the components of a more sophisticated chatbot. In the next section, we'll see how to build a ChatGPT-like app using OpenAI.
Build a ChatGPT-like app

Now that you've understood the basics of Streamlit's chat elements, let's make a few tweaks to it to build our own ChatGPT-like app. You'll need to install the OpenAI Python library and get an API key to follow along.
Install dependencies

First let's install the dependencies we'll need for this section:
pip install openai streamlit
Add OpenAI API key to Streamlit secrets

Next, let's add our OpenAI API key to Streamlit secrets. We do this by creating .streamlit/secrets.toml file in our project directory and adding the following lines to it:
# .streamlit/secrets.toml
OPENAI_API_KEY = "YOUR_API_KEY"
Write the app

Now let's write the app. We'll use the same code as before, but we'll replace the list of responses with a call to the OpenAI API. We'll also add a few more tweaks to make the app more ChatGPT-like.
import streamlit as st
from openai import OpenAI

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

All that's changed is that we've added a default model to st.session_state and set our OpenAI API key from Streamlit secrets. Here's where it gets interesting. We can replace our emulated stream with the model's responses from OpenAI:
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

Above, we've replaced the list of responses with a call to OpenAI().chat.completions.create. We've set stream=True to stream the responses to the frontend. In the API call, we pass the model name we hardcoded in session state and pass the chat history as a list of messages. We also pass the role and content of each message in the chat history. Finally, OpenAI returns a stream of responses (split into chunks of tokens), which we iterate through and display each chunk.

Putting it all together, here's the full code for our ChatGPT-like app and the result:
View full code
expand_more
Built with Streamlit 🎈
Fullscreen
open_in_new

Congratulations! You've built your own ChatGPT-like app in less than 50 lines of code.

We're very excited to see what you'll build with Streamlit's chat elements. Experiment with different models and tweak the code to build your own conversational apps. If you build something cool, let us know on the Forum or check out some other Generative AI apps for inspiration. 🎈

---

Build an LLM app using LangChain
OpenAI, LangChain, and Streamlit in 18 lines of code

In this tutorial, you will build a Streamlit LLM app that can generate text from a user-provided prompt. This Python app will use the LangChain framework and Streamlit. Optionally, you can deploy your app to Streamlit Community Cloud when you're done.

This tutorial is adapted from a blog post by Chanin Nantesanamat: LangChain tutorial #1: Build an LLM-powered app in 18 lines of code.
Built with Streamlit 🎈
Fullscreen
open_in_new
Objectives

    Get an OpenAI key from the end user.
    Validate the user's OpenAI key.
    Get a text prompt from the user.
    Authenticate OpenAI with the user's key.
    Send the user's prompt to OpenAI's API.
    Get a response and display it.

Bonus: Deploy the app on Streamlit Community Cloud!
Prerequisites

    Python 3.9+
    Streamlit
    LangChain
    OpenAI API key

Setup coding environment

In your IDE (integrated coding environment), open the terminal and install the following two Python libraries:
pip install streamlit langchain-openai

Create a requirements.txt file located in the root of your working directory and save these dependencies. This is necessary for deploying the app to the Streamlit Community Cloud later.
streamlit
openai
langchain
Building the app

The app is only 18 lines of code:
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

st.title("🦜🔗 Quickstart App")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    st.info(model.invoke(input_text))


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)

To start, create a new Python file and save it as streamlit_app.py in the root of your working directory.

    Import the necessary Python libraries.
    import streamlit as st
    from langchain_openai.chat_models import ChatOpenAI

    Create the app's title using st.title.
    st.title("🦜🔗 Quickstart App")

    Add a text input box for the user to enter their OpenAI API key.
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    Define a function to authenticate to OpenAI API with the user's key, send a prompt, and get an AI-generated response. This function accepts the user's prompt as an argument and displays the AI-generated response in a blue box using st.info.
    def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
        st.info(model.invoke(input_text))

    Finally, use st.form() to create a text box (st.text_area()) for user input. When the user clicks Submit, the generate-response() function is called with the user's input as an argument.
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            "What are the three key pieces of advice for learning how to code?",
        )
        submitted = st.form_submit_button("Submit")
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if submitted and openai_api_key.startswith("sk-"):
            generate_response(text)

    Remember to save your file!

    Return to your computer's terminal to run the app.
    streamlit run streamlit_app.py

Deploying the app

To deploy the app to the Streamlit Cloud, follow these steps:

    Create a GitHub repository for the app. Your repository should contain two files:
    your-repository/
    ├── streamlit_app.py
    └── requirements.txt

    Go to Streamlit Community Cloud, click the New app button from your workspace, then specify the repository, branch, and main file path. Optionally, you can customize your app's URL by choosing a custom subdomain.

    Click the Deploy! button.

Your app will now be deployed to Streamlit Community Cloud and can be accessed from around the world! 🌎
Conclusion

Congratulations on building an LLM-powered Streamlit app in 18 lines of code! 🥳 You can use this app to generate text from any prompt that you provide. The app is limited by the capabilities of the OpenAI LLM, but it can still be used to generate some creative and interesting text.

We hope you found this tutorial helpful! Check out more examples to see the power of Streamlit and LLM. 💖

Happy Streamlit-ing! 🎈

---
Collect user feedback about LLM responses

A common task in a chat app is to collect user feedback about an LLM's responses. Streamlit includes st.feedback to conveniently collect user sentiment by displaying a group of selectable sentiment icons.

This tutorial uses Streamlit's chat commands and st.feedback to build a simple chat app that collects user feedback about each response.
Applied concepts

    Use st.chat_input and st.chat_message to create a chat interface.
    Use st.feedback to collect user sentiment about chat responses.

Prerequisites

    This tutorial requires the following version of Streamlit:
    streamlit>=1.42.0

    You should have a clean working directory called your-repository.

    You should have a basic understanding of Session State.

Summary

In this example, you'll build a chat interface. To avoid API calls, the chat app will echo the user's prompt within a fixed response. Each chat response will be followed by a feedback widget where the user can vote "thumb up" or "thumb down." In the following code, a user can't change their feedback after it's given. If you want to let users change their rating, see the optional instructions at the end of this tutorial.

Here's a look at what you'll build:
Complete code
expand_more
Built with Streamlit 🎈
Fullscreen
open_in_new
Build the example
Initialize your app

    In your_repository, create a file named app.py.

    In a terminal, change directories to your_repository, and start your app:
    streamlit run app.py

    Your app will be blank because you still need to add code.

    In app.py, write the following:
    import streamlit as st
    import time

    You'll use time to build a simulated chat response stream.

    Save your app.py file, and view your running app.

    In your app, select "Always rerun", or press the "A" key.

    Your preview will be blank but will automatically update as you save changes to app.py.

    Return to your code.

Build a function to simulate a chat response stream

To begin, you'll define a function to stream a fixed chat response. You can skip this section if you just want to copy the function.
Complete function to simulate a chat stream
expand_more

    Define a function which accepts a prompt and formulates a response:
    def chat_stream(prompt):
        response = f'You said, "{prompt}" ...interesting.'

    Loop through the characters and yield each one at 0.02-second intervals:
        for char in response:
            yield char
            time.sleep(.02)

You now have a complete generator function to simulate a chat stream object.
Initialize and render your chat history

To make your chat app stateful, you'll save the conversation history into Session State as a list of messages. Each message is a dictionary of message attributes. The dictionary keys include the following:

    "role": Indicates the source of the message (either "user" or "assistant").
    "content": The body of the message as a string.
    "feedback": An integer that indicates a user's feedback. This is only included when the message role is "assistant" because users do not leave feedback on their own prompts.

    Initialize the chat history in Session State:
    if "history" not in st.session_state:
        st.session_state.history = []

    Iterate through the messages in your chat history and render their contents in chat message containers:
    for i, message in enumerate(st.session_state.history):
        with st.chat_message(message["role"]):
            st.write(message["content"])

    In a later step, you'll need a unique key for each assistant message. You can use the index of the message in your chat history to create a unique key. Therefore, use enumerate() to get an index along with each message dictionary.

    For each assistant message, check whether feedback has been saved:
            if message["role"] == "assistant":
                feedback = message.get("feedback", None)

    If no feedback is saved for the current message, the .get() method will return the specified default of None.

    Save the feedback value into Session State under a unique key for that message:
                st.session_state[f"feedback_{i}"] = feedback

    Because the message index within the ordered chat history is unique, you can use the index as the key. For readability, you can add a prefix, "feedback_", to the index. In the next step, to make the feedback widget show this value, you'll assign the same key to the widget.

    Add a feedback widget to the chat message container:
                st.feedback(
                    "thumbs",
                    key=f"feedback_{i}",
                    disabled=feedback is not None,
                )

    The code you've written so far will show the chat history. If a user has already rated a message in the chat history, the feedback widget will show the rating and be disabled. The user won't be able to change their rating.

    All unrated messages include an enabled feedback widget. However, if a user interacts with one of those widgets, there is no code to save that information into the chat history yet. To solve this, use a callback as shown in the following steps.

    At the top of your app, after the definition of chat_stream() and before you initialize your chat history, define a function to use as a callback:
    def save_feedback(index):
        st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]

    The save_feedback() function accepts an index and uses the index to get the associated widget value from Session State. Then, this value is saved into chat history.

    Add the callback and index argument to your st.feedback widget:
                st.feedback(
                    "thumbs",
                    key=f"feedback_{i}",
                    disabled=feedback is not None,
    +               on_change=save_feedback,
    +               args=[i],
                )

    When a user interacts with the feedback widget, the callback will update the chat history before the app reruns.

Add chat input

    Accept the user's prompt from an st.chat_input widget, display it in a chat message container, and then save it to the chat history:
    if prompt := st.chat_input("Say something"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

    The st.chat_input widget acts like a button. When a user enters a prompt and clicks the send icon, it triggers a rerun. During the rerun, the previous code displays the chat history. When this conditional block is executed, the user's new prompt is displayed and then added to the history. On the next rerun, this prompt will be displayed as part of the history.

    The := notation is shorthand to assign a variable within an expression. The following code is equivalent to the previous code in this step:
    prompt = st.chat_input("Say something")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

    In another chat message container, process the prompt, display the response, add a feedback widget, and append the response to the chat history:
       with st.chat_message("assistant"):
           response = st.write_stream(chat_stream(prompt))
           st.feedback(
               "thumbs",
               key=f"feedback_{len(st.session_state.history)}",
               on_change=save_feedback,
               args=[len(st.session_state.history)],
           )
       st.session_state.history.append({"role": "assistant", "content": response})

    This is the same pattern used for the user's prompt. Within the body of the conditional block, the response is displayed and then added to the history. On the next rerun, this response will be displayed as a part of the chat history.

    When Streamlit executes the st.feedback command, the response is not yet added to the chat history. Use an index equal to the length of the chat history because that is the index that the response will have when it's added to the chat history on the next line.

    Save your file and go to your browser to try your new app.

Optional: Change the feedback behavior

Your app currently allows users to rate any response once. They can submit their rating at any time, but can't change it.

If you want users to rate only the most recent response, you can remove the widgets from the chat history:
  for i, message in enumerate(st.session_state.history):
      with st.chat_message(message["role"]):
          st.write(message["content"])
-         if message["role"] == "assistant":
-             feedback = message.get("feedback", None)
-             st.session_state[f"feedback_{i}"] = feedback
-             st.feedback(
-                 "thumbs",
-                 key=f"feedback_{i}",
-                 disabled=feedback is not None,
-                 on_change=save_feedback,
-                 args=[i],
-             )

Or, if you want to allow users to change their responses, you can just remove the disabled parameter:
  for i, message in enumerate(st.session_state.history):
      with st.chat_message(message["role"]):
          st.write(message["content"])
          if message["role"] == "assistant":
              feedback = message.get("feedback", None)
              st.session_state[f"feedback_{i}"] = feedback
              st.feedback(
                  "thumbs",
                  key=f"feedback_{i}",
-                 disabled=feedback is not None,
                  on_change=save_feedback,
                  args=[i],
              )
