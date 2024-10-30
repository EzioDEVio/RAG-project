import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            text = load_pdf(os.path.join(folder_path, filename))
            documents.append({"filename": filename, "text": text})
    return documents
