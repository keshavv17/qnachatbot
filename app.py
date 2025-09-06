import streamlit as st
import openai 
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

### langsmith tracking
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING'] = os.getenv('LANGSMITH_TRACING')
os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT')

## prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant, please respond to the user queries"),
    ("user", "question:{question}")
])

def generate_response(question, api_key, llm, temperature, max_tokens):
      openai.api_key = api_key
      llm = ChatOpenAI(model = llm)
      output_parser = StrOutputParser()
      chain = prompt | llm | output_parser
      answer = chain.invoke({"question":question})
      return answer 
  
## Title of api
st.title("QnA chatbot with openai")
  
## sidebar for settings
st.sidebar.title("settings")
api_key = st.sidebar.text_input("Enter your openAI api key: ", type="password")

## drop down to select models
llm = st.sidebar.selectbox("Select an OpenAI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

## adjust reponse parameter
temperature = st.sidebar.slider("Temperature", min_value = 0.0, max_value = 1.0, value = 0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value = 50, max_value = 300, value = 150)

## define the main interface
st.write("go ahead and ask question")
user_input = st.text_input("You: ")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")