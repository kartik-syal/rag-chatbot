Certainly! Below is a comprehensive README for your project.

---

# RAG Chatbot for Oil Well Design Specifications

This project implements a Retrieval-Augmented Generation (RAG) chatbot that can search through PDF documents containing design specifications for oil wells and respond to user queries. The solution is scalable and supports searching thousands of documents.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [Environment Variables](#environment-variables)
- [License](#license)

## Features
- Load and process PDF documents
- Store document content and metadata in a vector store
- Retrieve relevant document content based on user queries
- Generate responses using OpenAI's GPT model
- Provide informative answers including context from the retrieved documents

## Prerequisites
- Python 3.10+
- Node.js and npm (for the frontend)
- pip (Python package installer)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/kartik-syal/rag-chatbot.git
    cd rag-chatbot
    ```

2. **Setup Backend**:
    - Navigate to the `backend` directory:
      ```bash
      cd backend
      ```

    - Create a virtual environment and activate it:
      ```bash
      python -m venv venv
      source venv/bin/activate
      ```

    - Install the required Python packages:
      ```bash
      pip install -r requirements.txt
      ```

3. **Setup Frontend**:
    - Navigate to the `frontend` directory:
      ```bash
      cd frontend
      ```

    - Install the required Node.js packages:
      ```bash
      npm install
      ```

## Running the Project

1. **Configure Environment Variables**:
    - Create a `.env` file in the `backend` directory with the following content:
      ```env
      OPENAI_API_KEY=your_openai_api_key
      ```

2. **Start the Backend**:
    - Navigate to the `backend` directory (if not already there):
      ```bash
      cd backend
      ```

    - Run the FastAPI server:
      ```bash
      python app.py
      ```

3. **Start the Frontend**:
    - Navigate to the `frontend` directory:
      ```bash
      cd frontend
      ```

    - Run the Streamlit app:
      ```bash
      streamlit run streamlit_app.py
      ```

## Project Structure

```
rag-chatbot/
│
├── backend/
│   ├── .env
│   ├── app.py
│   ├── requirements.txt
│   └── model/
│       ├── document_processing.py
│       ├── rag_chain.py
│       └── __init__.py
│
└── frontend/
    ├── streamlit_app.py
    └── package.json
```

## Usage

- **Query the Chatbot**:
  - Use the frontend interface to input queries about the oil well design specifications.
  - The chatbot will retrieve relevant information from the documents and generate a response.

## Example Queries

- **Compare high-pressure separator specifications across wells**:
  - Sample query: "Compare high-pressure separator specifications across these wells and identify key differences - VOSS 14-11H, RECKARD 31-27H, KUPPER 34-10H"
  
- **Compare export pump specifications across wells**:
  - Sample query: "Compare export pump specifications across these wells and identify key differences."

- **Extract a diagram from the document**:
  - Sample query: "Extract a diagram from the document."

## Environment Variables

The project uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for accessing the GPT model.