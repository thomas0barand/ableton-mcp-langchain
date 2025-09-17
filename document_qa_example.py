"""
LangChain Document Q&A Example
This demonstrates document loading, chunking, and retrieval-augmented generation with Google Gemini
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Make sure to set your GOOGLE_API_KEY environment variable")

def document_qa_example():
    """Example of document-based question answering using LangChain with Google Gemini"""
    
    # Check if API key is available
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        print("Error: GOOGLE_API_KEY not set or still has placeholder value")
        print("Please set your Google API key in the .env file or as an environment variable")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    # Create a sample document
    sample_text = """
    LangChain is a framework for developing applications powered by language models. 
    It enables applications that are data-aware and agentic, meaning they can connect 
    to other sources of data and interact with their environment.
    
    Key features of LangChain include:
    1. LLMs and Prompts: LangChain makes it easy to swap out LLMs and manage prompts
    2. Chains: Combine LLMs and other components to create applications
    3. Data Augmented Generation: Use external data sources to augment LLM responses
    4. Agents: Use LLMs to decide what actions to take
    5. Memory: Persist application state between runs
    
    LangChain supports multiple LLM providers including OpenAI, Anthropic, and many others.
    It also provides tools for document loading, text splitting, vector stores, and retrieval.
    """
    
    # Save sample text to file
    with open("sample_document.txt", "w") as f:
        f.write(sample_text)
    
    try:
        # Load document
        loader = TextLoader("sample_document.txt")
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50
        )
        texts = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        vectorstore = FAISS.from_documents(texts, embeddings)
        
        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=api_key
        )
        
        # Create custom prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context:
        {context}

        Question: {question}
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        # Example questions
        questions = [
            "What is LangChain?",
            "What are the key features of LangChain?",
            "Which LLM providers does LangChain support?",
            "What is data augmented generation?"
        ]
        
        print("Document Q&A Example")
        print("=" * 50)
        
        for question in questions:
            print(f"\nQuestion: {question}")
            answer = qa_chain.run(question)
            print(f"Answer: {answer}")
            print("-" * 30)
    
    finally:
        # Clean up
        if os.path.exists("sample_document.txt"):
            os.remove("sample_document.txt")

if __name__ == "__main__":
    document_qa_example()
