import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS



load_dotenv()
st.header("My First Chatbot")

with st.sidebar:
     st.title("Your Documents")
     file = st.file_uploader("Upload a PDF File and start asking questions" , type="pdf")


### Extract Contents from pdf ###

if file is not None:
     #extract text from it
     with pdfplumber.open(file) as pdf:
          text = ""
          for page in pdf.pages:
               text+=page.extract_text() + "\n"
     # st.write(text)

### Split Text into chunks ###

     text_splitter = RecursiveCharacterTextSplitter(
          separators=["\n\n" , "\n" , ". " , " " , ""],
          chunk_size=1000,
          chunk_overlap=200
     )

     chunks = text_splitter.split_text(text)
     st.write(chunks)

### Embeddings ###

     embeddings = GoogleGenerativeAIEmbeddings(
          model = "models/gemini-embedding-001",
          google_api_key = os.getenv("GoogleAPIKey")
     )
# models/gemini-embedding-001
# models/gemini-embedding-2-preview

     vector_store = FAISS.from_texts(chunks, embeddings)
     st.write(vector_store)

# Get the User Question
     user_question = st.text_input("Type Your Question Here")

# Generate Answer
# CHAIN
# QUESTION -> EMBEDDINGS -> SIMILARITY SEARCH -> RESULTS TO LLM -> RESPONSE

     