import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from model.document_processing import load_and_split_documents
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths to the PDF files containing oil well design specifications
file_paths = [
    "../data/PFD-PID ROSEMARY 1 14H.pdf",
    "../data/PFD-PID VOSS 14-11H.pdf",
    "../data/PFD-PID RECKARD 31-27H.pdf"
]

# Load the documents, add metadata, and split into chunks
splits = load_and_split_documents(file_paths)

# Embed the documents and store them in a vector store
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"]))

# Create a retriever to fetch relevant documents based on user queries
retriever = vectorstore.as_retriever()

# Define the system prompt for the LLM
system_prompt = (
    "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise.\n\n"
    "{context}"
    "\n\n"
    "Sample Query:\n Compare high-pressure separator specifications across these wells and identify key differences - \"BRADLEY 22-15H\", \"WINTERS 39-18H\", \"LEWIS 12-09H\"\n\n"
    "Sample Response:\n"
    "BRADLEY 22-15H\n"
    "Size: 72\" I.D. (1.83 M) x 20'-0\" S/S (6.10 M)\n"
    "Design Pressure: 1500 PSIG (103.4 BAR)/FV at 325°F (163°C)\n"
    "Operating Pressure: 400 PSIG (27.6 BAR) at 75°F (24°C)\n"
    "Liquid Residence Time: 4 minutes\n\n"
    "WINTERS 39-18H\n"
    "Size: 72\" I.D. (1.83 M) x 20'-0\" S/S (6.10 M)\n"
    "Design Pressure: 1500 PSIG (103.4 BAR)/FV at 325°F (163°C)\n"
    "Operating Pressure: 425 PSIG (29.3 BAR) at 80°F (27°C)\n"
    "Liquid Residence Time: 3.5 minutes\n\n"
    "LEWIS 12-09H\n"
    "Size: 72\" I.D. (1.83 M) x 20'-0\" S/S (6.10 M)\n"
    "Design Pressure: 1500 PSIG (103.4 BAR)/FV at 325°F (163°C)\n"
    "Operating Pressure: 375 PSIG (25.9 BAR) at 70°F (21°C)\n"
    "Liquid Residence Time: 3 minutes"
    "\n\n"
    "Key Differences\n"
    "Upon review, the high-pressure separator specifications for the wells BRADLEY 22-15H, WINTERS 39-18H, and LEWIS 12-09H exhibit variations primarily in their operating pressures and liquid residence times. While all separators share the same size and design pressure, WINTERS 39-18H operates at a higher pressure and slightly shorter liquid residence time compared to BRADLEY 22-15H and LEWIS 12-09H."
)

# Create the prompt template for the LLM
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o", openai_api_key=os.environ["OPENAI_API_KEY"])

class RAGChain:
    """
    Class to define the Retrieval-Augmented Generation (RAG) chain.
    It integrates document retrieval and LLM to generate answers based on user queries.
    """
    def __init__(self, retriever, llm, prompt_template):
        self.retriever = retriever
        self.llm = llm
        self.prompt_template = prompt_template

    def invoke(self, inputs):
        """
        Invoke the RAG chain to process a user query and generate an answer.
        
        Parameters:
        inputs (dict): Dictionary containing the user query.
        
        Returns:
        dict: Dictionary containing the answer and context.
        """
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
