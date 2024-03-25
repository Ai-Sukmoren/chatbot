import streamlit as st
from utilities.agent import generate_response
from time import sleep

def write_message(role, content, save=True):
    """This is a helper function that saves a message to the session state and then writes a message to the UI."""
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    if role == "assistant":
        with st.chat_message(role, avatar="🤖"):
            st.markdown(content)
    else:
        with st.chat_message(role, avatar="😖"):
            st.markdown(content)

def handle_submit(message):
    """Handles user input, generates a response, and updates the UI."""
    with st.spinner('Thinking...'):
        response = generate_response(message)
        sleep(1)  # Simulate processing time
        write_message('assistant', response)

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if __name__ == '__main__':
    # Initialize the Streamlit UI layout.
    st.set_page_config(page_title='Jarvis', page_icon='🤖', layout='centered')

    # Display the title and description of the chatbot.
    with st.container():
        st.title("Animes Chatbot using OpenAI")
        st.markdown("""
            You can ask the 🤖 about: 
            - Animme details and Genres 
            - Recommend YouTube video based on your anime input

            **The chatbot is designed to be used for asking anime related question and YouTube serch.**
            """)

    # Initialize session state for storing messages if not already done.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm your anime expert assistant Chatbot! How can I help you?"}]

    # Display messages from the session state.
    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)

    # Handle user input through chat input box.
    if prompt := st.chat_input("Ask me something"):
        write_message('user', prompt)
        handle_submit(prompt)
