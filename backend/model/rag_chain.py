import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from model.document_processing import load_and_split_documents
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths to your PDF files
file_paths = [
    "../data/PFD-PID ROSEMARY 1 14H.pdf",
    "../data/PFD-PID VOSS 14-11H.pdf",
    "../data/PFD-PID RECKARD 31-27H.pdf"
]

# Load and split documents
splits = load_and_split_documents(file_paths)

# Embed and store documents
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"]))

# Create retriever
retriever = vectorstore.as_retriever()

# System prompt
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise."
    "\n\n"
    "{context}"
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.environ["OPENAI_API_KEY"])

# Define the RAG chain manually
class RAGChain:
    def __init__(self, retriever, llm, prompt_template):
        self.retriever = retriever
        self.llm = llm
        self.prompt_template = prompt_template

    def invoke(self, inputs):
        query = inputs["input"]
        retrieved_docs = self.retriever.invoke(query)
        context = "\n\n\n".join([
            f"Below are the details for Oil Well Named: {doc.metadata['oil-well-name']}\n\n{doc.page_content}"
            for doc in retrieved_docs
        ])
        print(context)
        prompt_content = self.prompt_template.format(context=context, input=query)
        
        messages = [
            SystemMessage(content=prompt_content),
            HumanMessage(content=query),
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        return {"answer": answer, "context": retrieved_docs}

# Instantiate the RAG chain
rag_chain = RAGChain(retriever, llm, prompt)
