import streamlit as st
from utilities.agent import generate_response


# Page Config
st.set_page_config("Jarvis", page_icon= "👾")

# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the anime experts Chatbot!  How can I help you?"},
    ]

def write_message(role, content, save = True):
    """
    This is a helper function that saves a message to the
     session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    if role == "assistant":
        with st.chat_message(role, avatar = "👾"):
            st.markdown(content)
    else:
        with st.chat_message(role):
            st.markdown(content)

# Submit handler
def handle_submit(message):
    # Handle the response
    with st.spinner('Thinking...'):
        response = generate_response(message)
        from time import sleep
        sleep(1)
        write_message('assistant', response)
        
# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("ask me somthing"):
    # Display user message in chat message container
    write_message('user', prompt)

    # Generate a response
    handle_submit(prompt)

