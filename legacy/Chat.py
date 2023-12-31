import streamlit as st
from utils import scrape_website, text_to_pdf, upload_to_openai
from init import initialise_assistant
from config import assistant_id, instruction
import time
import openai
import os
from dotenv import load_dotenv
from mongodb_handler import insert_document


def Chat():
    load_dotenv()
    openai.api_key= os.getenv('OPENAI_API_KEY')
    client = openai
    # initialise_assistant()
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
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.write("thread id: ", thread.id)
    
    # Function to show the alternate sidebar
    st.sidebar.header("Required Details")
    name = st.sidebar.text_input("Name:*", key="Please Enter Your Name")
    email = st.sidebar.text_input("Email:*", key="Please Enter Your Email")
    if st.sidebar.button("Submit"):
            if name and email:
                # Insert data into MongoDB
                insert_document({"name": name, "email": email})
                st.sidebar.success("Data submitted successfully!")
                # st.session_state.show_alternate = True
                st.session_state.start_chat = True
                st.rerun()
            else:
                st.sidebar.error("Please fill in all the fields.")
        
    
        # show_alternate_sidebar()
    # if ((name == "") | (email == "")):
    #     st.sidebar.warning("Please enter your Name and Email")
    # else:
    #     # TODO: Implement Pushing to Databse
    #     pass
    # st.sidebar.header("Additional Features")
    # website_url = st.sidebar.text_input("Enter a website URL to scrape and organize into a PDF", key="website_url")
    
    # # Button to scrape a website, convert to PDF, and upload to OpenAI
    # if st.sidebar.button("Scrape and Upload"):
    #     # Scrape, convert, and upload process
    #     scraped_text = scrape_website(website_url)
    #     pdf_path = text_to_pdf(scraped_text, "scraped_content.pdf")
    #     file_id = upload_to_openai(pdf_path)
    #     st.session_state.file_id_list.append(file_id)
    #     #st.sidebar.write(f"File ID: {file_id}")

    # # Sidebar option for users to upload their own files
    # uploaded_file = st.sidebar.file_uploader("Upload a file to OpenAI embeddings", key="file_uploader")

    # # Button to upload a user's file and store the file ID
    # if st.sidebar.button("Upload File"):
    #     # Upload file provided by user
    #     if uploaded_file:
    #         with open(f"{uploaded_file.name}", "wb") as f:
    #             f.write(uploaded_file.getbuffer())
    #         additional_file_id = upload_to_openai(f"{uploaded_file.name}")
    #         st.session_state.file_id_list.append(additional_file_id)
    #         st.sidebar.write(f"Additional File ID: {additional_file_id}")

    # # Display all file IDs
    # if st.session_state.file_id_list:
        # st.sidebar.write("Uploaded File IDs:")
        # for file_id in st.session_state.file_id_list:
        #     st.sidebar.write(file_id)
        #     # Associate files with the assistant
        #     assistant_file = client.beta.assistants.files.create(
        #         assistant_id=assistant_id, 
        #         file_id=file_id
        #     )

    # Button to start the chat session
    # if st.sidebar.button("Start Chat"):
    #     if ((name == "") | (email == "")):
    #         st.sidebar.warning("Please enter your Name and Email")
    #     else:
    #     # Check if files are uploaded before starting chat
    #     # if st.session_state.file_id_list:
            
    #         # else:
    #         #     st.sidebar.warning("Please upload at least one file to start the chat.")


    # Define the function to process messages with citations
    def process_message_with_citations(message):
        """Extract content and annotations from the message and format citations as footnotes."""
        message_content = message.content[0].text
        # annotations = message_content.annotations if hasattr(message_content, 'annotations') else []
        # citations = []

        # # Iterate over the annotations and add footnotes
        # for index, annotation in enumerate(annotations):
        #     # Replace the text with a footnote
        #     message_content.value = message_content.value.replace(annotation.text, f' [{index + 1}]')

        #     # Gather citations based on annotation attributes
        #     if (file_citation := getattr(annotation, 'file_citation', None)):
        #         # Retrieve the cited file details (dummy response here since we can't call OpenAI)
        #         cited_file = {'filename': 'cited_document.pdf'}  # This should be replaced with actual file retrieval
        #         citations.append(f'[{index + 1}] {file_citation.quote} from {cited_file["filename"]}')
        #     elif (file_path := getattr(annotation, 'file_path', None)):
        #         # Placeholder for file download citation
        #         cited_file = {'filename': 'downloaded_document.pdf'}  # This should be replaced with actual file retrieval
        #         citations.append(f'[{index + 1}] Click [here](#) to download {cited_file["filename"]}')  # The download link should be replaced with the actual download path

        # Add footnotes to the end of the message content
        full_response = message_content.value
        return full_response

    # Main chat interface setup
    st.title("Welcome to TweetNet – Your Personal Twitter Content Assistant!")
    st.write("Elevate your Twitter strategy with our assistance. Whether your goal is to inform, entertain, or inspire, our bot crafts tweets that perfectly align with your vision.")

    # Only show the chat interface if the chat has been started
    if st.session_state.start_chat:
        # assistant_id_res = initialise_assistant()
        # Initialize the model and messages list if not already in session state
        # if "openai_model" not in st.session_state:
        #     st.session_state.openai_model = "gpt-3.5-turbo-1106"
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display existing messages in the chat
        for message in st.session_state.messages:
            print(message)
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input for the user
        if prompt := st.chat_input("What is up?"):
            # Add user message to the state and display it
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add the user's message to the existing thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )

            # Create a run with additional instructions
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_id,
                instructions=instruction
                )

            # Poll for the run to complete and retrieve the assistant's messages
            while run.status != 'completed':
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )

            # Retrieve messages added by the assistant
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

            # Process and display assistant messages
            assistant_messages_for_run = [
                message for message in messages 
                if message.run_id == run.id and message.role == "assistant"
            ]
            for message in assistant_messages_for_run:
                full_response = process_message_with_citations(message)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)
    else:
        st.sidebar.markdown(
             
        """
           
            #### 🌟 Get Started:
            Give TweetNet a try! Just a quick chat, and you’ll see how we can transform your Twitter experience. \n
            Enter your **Name** and **Email** to start.
        """
    )
        
        col1, col2, col3 = st.columns(3)
        # Prompt to start the chat
        with col1:
            st.markdown(
             
        """
            
            #### 🚀 Elevate Your Twitter Presence:
            Our bot helps you craft tweets that resonate with your audience. Whether you're aiming for professional, casual, or inspirational tweets, we've got you covered.

            #### 🎨 Visual Appeal Meets Precision:
            Create stunning images complemented by concise, accurate text. Perfectly tailored for Twitter's dynamic platform.
       """
    )
        with col2:
            st.markdown(
             
        """
            #### ✏️ Custom Content Creation:
            Just tell us your style - professional, humorous, informative? Our bot drafts engaging, relevant tweet scripts within the 280-character limit.

            #### 📊 Smart Analytics:
            After each tweet, get an instant word count. Track and refine your content strategy for maximum impact.

            """
    )
        with col3:
            st.markdown(
             
        """
            #### 🔍 Targeted Organic Growth:
            Our bot is not just about creating tweets; it's about building your brand. Gain organic reach, engagement, and followers. Watch as your community grow!

             """
    )
        

Chat()