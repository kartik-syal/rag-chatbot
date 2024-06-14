import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents(file_paths):
    docs = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        pdf_docs = loader.load()
        oil_well_name = os.path.splitext(os.path.basename(path))[0]  # Get the file name without path and extension
        if oil_well_name.startswith("PFD-PID"):
            oil_well_name = oil_well_name[len("PFD-PID "):]  # Remove the "PFD-PID" prefix
        for doc in pdf_docs:
            doc.metadata['oil-well-name'] = oil_well_name
        docs.extend(pdf_docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits
