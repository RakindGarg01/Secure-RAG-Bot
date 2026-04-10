import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()
st.header("My First Chatbot")

with st.sidebar:
     st.title("Your Documents")
     file = st.file_uploader("Upload a PDF File and start asking questions" , type="pdf")

# Get the User Question
user_question = st.text_input("Type Your Question Here") 

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
     # st.write(chunks)

     ### Embeddings ###

     embeddings = GoogleGenerativeAIEmbeddings(
          model = "models/gemini-embedding-001",
          google_api_key = os.getenv("GoogleAPIKey")
     )
     # models/gemini-embedding-001
     # models/gemini-embedding-2-preview

     vector_store = FAISS.from_texts(chunks, embeddings) 

     # Generate Answer
     # CHAIN = QUESTION -> EMBEDDINGS -> SIMILARITY SEARCH -> RESULTS TO LLM -> RESPONSE
     # Here Retriever is the Similarity Search in Other Words, It search among vector DB and find no. of corresponding results defined

     retriever = vector_store.as_retriever(
          search_type = "mmr", # It is similarity search
          search_kwargs = {"k" : 4 }  # It is finding 4 results corresponding to our Search Pattern
     )

     def format_docs(docs):
          return "\n\n".join([doc.page_content for doc in docs]) # Joining the 4 results to single output

     #Defining LLM

     llm = ChatGoogleGenerativeAI(
          model="gemini-2.5-flash",     # This is the LLM model which we want to use
          temperature=0.3,              # Temprature can be 0 ,1 ,2 or more.Idea is that as you go higher 0.5 , 0.8 , 1 , LLM will get more Random Answers.
          # Random Mean by it will start creating new answers If you are on lower side 0.1 , 0.2 the answer will be deterministic. It will be very close to PDF.
          max_tokens=1000,              # how many okens to generate in response
          google_api_key=os.getenv("GoogleAPIKey") # AUth Key
     )
     
     #provide the prompts
     prompt = ChatPromptTemplate.from_messages([
     ("system",
          "You are a helpful assistant answering questions about a PDF document.\n\n"
          "Guidelines:\n"
          "1. Provide complete, well-explained answers using the context below.\n"
          "2. Include relevant details, numbers, and explanations to give a thorough response.\n"
          "3. If the context mentions related information, include it to give fuller picture.\n"
          "4. Only use information from the provided context - do not use outside knowledge.\n"
          "5. Summarize long information, ideally in bullets where needed\n"
          "6. If the information is not in the context, say so politely.\n\n"
          "Context:\n{context}"),
     ("human", "{question}")
     ])

     chain = (
          {"context" : retriever | format_docs  , "question" : RunnablePassthrough()}
          | prompt
          | llm
          | StrOutputParser()
     )

     if user_question:
          response = chain.invoke(user_question)
          st.write(response)
     
