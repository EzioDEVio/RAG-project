import openai
import os
from dotenv import load_dotenv
from document_loader import load_documents_from_folder
from retriever import create_index, retrieve_documents

load_dotenv()

# Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(query, retrieved_docs):
    # Prepare the context from retrieved documents
    context = "\n\n".join([doc["text"][:1000] for doc in retrieved_docs])

    # OpenAI API call with `gpt-3.5-turbo`
    messages = [
        {"role": "system", "content": "You are a helpful assistant for answering questions based on provided documents."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        temperature=0.3,
    )
    return response.choices[0].message['content'].strip()
