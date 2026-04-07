import streamlit as st
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

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