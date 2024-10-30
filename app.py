import streamlit as st
import os
import shutil
from document_loader import load_documents_from_folder
from retriever import create_index, retrieve_documents
from main import generate_response

# Directory to store uploaded files
UPLOAD_FOLDER = "data/uploaded_pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Custom CSS for a modern look
st.markdown(
    """
    <style>
    /* General layout */
    .block-container {
        max-width: 800px;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    /* Buttons */
    .stButton > button {
        background-color: #0073e6;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 16px;
    }
    /* Text input and file uploader */
    .stTextInput, .stFileUploader {
        font-size: 16px;
    }
    /* Headings */
    h1, h2, h3 {
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and description
st.title("EzioDevIo RAG")
st.write("Upload a PDF, then ask questions based on its content. Get responses in real-time!")

# Sidebar for file upload and clear options
st.sidebar.header("Options")

# Initialize session state for question, answer, and file clearing
if "query" not in st.session_state:
    st.session_state.query = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "clear_files" not in st.session_state:
    st.session_state.clear_files = False

# Define a function to clear the question input and answer
def clear_question():
    st.session_state.query = ""
    st.session_state.answer = ""

# File uploader
uploaded_files = st.sidebar.file_uploader("Upload PDF(s)", type=["pdf"], accept_multiple_files=True, key="file_uploader")

# Clear files button in sidebar
if st.sidebar.button("Clear Uploaded Files"):
    shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    st.session_state.clear_files = True  # Trigger flag to clear files
    st.session_state.query = ""  # Clear any question
    st.session_state.answer = ""  # Clear any answer
    st.sidebar.success("Uploaded files cleared!")

# Reset the file uploader if clear_files flag is set
if st.session_state.clear_files:
    uploaded_files = None
    st.session_state.clear_files = False  # Reset the flag

# Process files if uploaded
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("Files uploaded successfully!")

    # Load and index documents
    documents = load_documents_from_folder(UPLOAD_FOLDER)
    faiss_index = create_index(documents)

    # Input section
    st.subheader("Ask a Question")
    st.text_input("Enter your question here:", value=st.session_state.query, key="query")

    # "Clear Question" button functionality with callback
    st.button("Clear Question", on_click=clear_question)

    # Get Answer button
    if st.button("Get Answer"):
        if st.session_state.query:
            # Retrieve and generate answer
            retrieved_docs = retrieve_documents(st.session_state.query, faiss_index)
            st.session_state.answer = generate_response(st.session_state.query, retrieved_docs)
        else:
            st.warning("Please enter a question.")

    # Display the answer if available
    if st.session_state.answer:
        st.write("### Answer:")
        st.write(st.session_state.answer)
else:
    st.info("Upload one or more PDF files to begin.")
