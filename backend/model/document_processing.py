import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents(file_paths):
    """
    Load PDF documents, extract text, assign metadata, and split text into chunks.
    
    Parameters:
    file_paths (list): List of file paths to the PDF documents.
    
    Returns:
    list: List of text chunks with metadata.
    """
    docs = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        pdf_docs = loader.load()
        # Extract file name without path and extension
        oil_well_name = os.path.splitext(os.path.basename(path))[0]
        # Remove "PFD-PID" prefix if present
        if oil_well_name.startswith("PFD-PID"):
            oil_well_name = oil_well_name[len("PFD-PID "):]
        # Add metadata to each document
        for doc in pdf_docs:
            doc.metadata['oil-well-name'] = oil_well_name
        docs.extend(pdf_docs)

    # Split documents into smaller chunks for better processing
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits
