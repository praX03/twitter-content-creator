# Import necessary libraries
import openai
import streamlit as st
from bs4 import BeautifulSoup
import requests
import pdfkit
import time
from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key= os.getenv('OPENAI_API_KEY')
# Set your OpenAI Assistant ID here
assistant_id = 'asst_2wGjCp2rUUBf1SYLkXoL6MOn'
instruction="As a 'Twitter Content Creator', your key responsibility is to assist users in crafting engaging, platform-appropriate content for Twitter. This role involves creating visually appealing images with minimal text, verifying the accuracy of any text included. You are expected to engage with users to understand their desired content type, which may vary from professional to casual, humorous, informative, or inspirational themes. Your focus will include drafting tweet scripts that are relevant, captivating, and tailored for the Twitter audience. Draft relevant, engaging tweet scripts within a 280-character limit. Following each interaction, summarize your understanding of the user's requirements, assigning a confidence score from 0 to 100 to indicate your assurance in meeting their needs. You should make 3 tweets and take user's opinion, based on their opinion you should choose the leading tweet. Adaptability to the unique context of each user's request is crucial, aiming to deliver optimal, Twitter-specific content while maximizing user satisfaction. Your role extends to creating posts that drive organic reach, engagement, and profile visits, fostering a growing follower base. These followers enhance our domain authority, amplifying our influence over the audience and fostering a vibrant community. At the beginning of each conversation, warmly welcome the user and succinctly describe your capabilities, encouraging them to engage with your services for their Twitter content needs."# Initialize the OpenAI client (ensure to set your API key in the sidebar within the app)
client = openai

# def initialise_assistant():
#     assistant = client.beta.assistants.create(
#         name="Twitter Content Creator API",
#         instructions=instruction,
#         # tools=[{"type": "function_calling"}],
#         model="gpt-3.5-turbo-1106"
#     )
#     print(assistant.id)
#     return assistant.id

# Initialize session state variables for file IDs and chat control
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Set up the Streamlit page with a title and icon
st.set_page_config(page_title="Twitter Content Creator", page_icon=":speech_balloon:")

# Define functions for scraping, converting text to PDF, and uploading to OpenAI
def scrape_website(url):
    """Scrape text from a website URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def text_to_pdf(text, filename):
    """Convert text content to a PDF file."""
    path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(text, filename, configuration=config)
    return filename

def upload_to_openai(filepath):
    """Upload a file to OpenAI and return its file ID."""
    with open(filepath, "rb") as file:
        response = openai.files.create(file=file.read(), purpose="assistants")
    return response.id

# Create a sidebar for API key configuration and additional features
# st.sidebar.header("Configuration")
# api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
# if api_key:
#     openai.api_key = api_key

# Additional features in the sidebar for web scraping and file uploading
# st.sidebar.header("Required Details")

# if st.sidebar.button("Submit"):
    # if ((name == "") | (email == "")):
    #     st.sidebar.warning("Please enter your Name and Email")
    # else:
    #     # TODO: Implement Pushing to Databse
    #     pass
# st.sidebar.header("Additional Features")
# website_url = st.sidebar.text_input("Enter a website URL to scrape and organize into a PDF", key="website_url")

# Button to scrape a website, convert to PDF, and upload to OpenAI
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
#     st.sidebar.write("Uploaded File IDs:")
#     for file_id in st.session_state.file_id_list:
#         st.sidebar.write(file_id)
#         # Associate files with the assistant
#         assistant_file = client.beta.assistants.files.create(
#             assistant_id=assistant_id, 
#             file_id=file_id
#         )

# Button to start the chat session
if st.sidebar.button("Start Chat"):
    
    st.session_state.start_chat = True
    # Create a thread once and store its ID in session state
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.write("thread id: ", thread.id)
    # else:
    #     st.sidebar.warning("Please upload at least one file to start the chat.")

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
st.title("Twitter Content Creator")
st.write("I can create your posts and content for you")

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
    # Prompt to start the chat
    # name = st.sidebar.text_input("Name:*", key="Please Enter Your Name")
    # email = st.sidebar.text_input("Email:*", key="Please Enter Your Email")
    # if ((name == "") | (email == "")):
    #     st.sidebar.warning("Please enter your Name and Email")
    
    st.write("Please click 'Start Chat' to begin the conversation.")