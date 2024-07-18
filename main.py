import streamlit as st
from utilities.agent import generate_response
from time import sleep

class AnimeChatbot:
    def __init__(self):
        self.init_ui()
        self.init_session_state()
        self.display_logo()
        self.display_title()
        self.display_description()
        self.display_messages()
        self.handle_user_input()

    def init_ui(self):
        st.set_page_config(page_title='Anime Chatbot', page_icon='🤖', layout='centered')

    def init_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm your anime expert assistant Chatbot! How can I help you?"}]

    def display_logo(self):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image('pic\\image.png', width=200)  # Adjust the path as needed

    def display_title(self):
        st.title("Anime Chatbot using OpenAI")

    def display_description(self):
        st.markdown("""
            You can ask the 🤖 about: 
            - Anime details and genres 
            - Recommend YouTube videos based on your anime input

            **The chatbot is designed to be used for asking anime-related questions and YouTube searches.**
            """)

    def display_messages(self):
        for message in st.session_state.messages:
            self.write_message(message['role'], message['content'], save=False)

    def write_message(self, role, content, save=True):
        """Saves a message to the session state and writes a message to the UI."""
        if save:
            st.session_state.messages.append({"role": role, "content": content})

        avatar = "🤖" if role == "assistant" else "😖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)

    def handle_submit(self, message):
        """Handles user input, generates a response, and updates the UI."""
        with st.spinner('Thinking...'):
            response = generate_response(message)
            sleep(1)  # Simulate processing time
            self.write_message('assistant', response)

    def handle_user_input(self):
        if prompt := st.chat_input("Ask me something"):
            self.write_message('user', prompt)
            self.handle_submit(prompt)

    @staticmethod
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.sidebar.button('Clear Chat History', on_click=AnimeChatbot.clear_chat_history)


if __name__ == '__main__':
    AnimeChatbot()
