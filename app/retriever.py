from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 3})