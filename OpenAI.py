import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv

load_dotenv()

## Loading the GROQ and OPEN PAPI KEY

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv('GROQ_API_KEY')

st.title("Chat_Groq_with_Llam3_Demo")

llm = ChatGroq(groq_api_key=groq_api_key,
               model_name="llama3-8b-8192")
prompt= ChatPromptTemplate.from_template(
    """Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}"""
)

def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("./Researchpapers")
        st.session_state.documents = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap =200)
        st.session_state.final_file = st.session_state.text_splitter.split_documents(st.session_state.documents[0:20])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_file,st.session_state.embeddings)

prompt1 = st.text_input("Write your query over here")

if st.button("Document Embeddings"):
    vector_embedding()
    st.write("Vectorestore database is ready")

import time


if prompt1:
    start =  time.process_time()
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response = retrieval_chain.invoke({'input':prompt1})
    print("Response time :", time.process_time()-start)
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i,doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("----------------")