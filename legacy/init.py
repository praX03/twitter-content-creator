import streamlit as st

def initialise_assistant():
    

    # def initialise_assistant():
    #     assistant = client.beta.assistants.create(
    #         name="Twitter Content Creator API",
    #         instructions=instruction,
    #         # tools=[{"type": "function_calling"}],
    #         model="gpt-3.5-turbo-1106"
    #     )
    #     print(assistant.id)
    #     return assistant.id
    # Initialize the session state
    if 'page' not in st.session_state:
        st.session_state.page = 'entry'

    # Initialize session state variables for file IDs and chat control
    if "file_id_list" not in st.session_state:
        st.session_state.file_id_list = []

    if "start_chat" not in st.session_state:
        st.session_state.start_chat = False

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    if 'show_alternate' not in st.session_state:
            st.session_state.show_alternate = False
    return(st.session_state.page, st.session_state.file_id_list, st.session_state.start_chat, st.session_state.thread_id)