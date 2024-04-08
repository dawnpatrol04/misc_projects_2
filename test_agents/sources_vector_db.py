# Install necessary dependencies
# Note: This line is meant to be run in a Jupyter Notebook or similar environment. For a standalone script, run this command in your terminal.
# %pip install --upgrade --quiet langchain langchain-community langchainhub langchain-openai chromadb bs4

# Setting up environment variables
import getpass
import os

# Set your OpenAI API key here
# os.environ["OPENAI_API_KEY"] = getpass.getpass()  # Or replace `getpass.getpass()` with your actual API key in quotes

# Uncomment below lines if you prefer loading the API key from a .env file
import dotenv
dotenv.load_dotenv()

# Optionally set up LangSmith for logging traces
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()  # Or replace `getpass.getpass()` with your actual LangChain API key in quotes

# Import necessary modules
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import  ChatVertexAI , VertexAIEmbeddings

# Function to load, chunk, and index the blog content
def load_and_prepare_content():
    bs_strainer = bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))
    loader = WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",), bs_kwargs={"parse_only": bs_strainer})
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=VertexAIEmbeddings(model_name="textembedding-gecko"))
    return vectorstore.as_retriever()

# Define function to format documents for display
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Setting up the Q&A chain without sources
def setup_chain_without_sources(retriever):
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatVertexAI(model_name="gemini-pro", temperature=0)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# Setting up the chain with sources
def setup_chain_with_sources(retriever):
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatVertexAI(model_name="gemini-pro", temperature=0)
    
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )
    
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)
    
    return rag_chain_with_source

# Main function to run the demo
def main():
    retriever = load_and_prepare_content()
    
    # Chain without sources
    rag_chain = setup_chain_without_sources(retriever)
    answer_without_sources = rag_chain.invoke("What is Task Decomposition?")
    print("Answer without sources:", answer_without_sources)
    
    # Chain with sources
    rag_chain_with_source = setup_chain_with_sources(retriever)
    answer_with_sources = rag_chain_with_source.invoke("What is Task Decomposition")
    print("Answer with sources:", answer_with_sources)

if __name__ == "__main__":
    main()
