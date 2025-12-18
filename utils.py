import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 1. Environment variables load karna (wo secret key uthana)
load_dotenv()

# 2. Google ka AI Model configure karna
# Hum 'gemini-pro' use kar rahe hain jo text ke liye best free model hai
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3 # Temperature kam rakha hai taaki AI creative na ho, balki accurate ho
)

# --- Function 1: PDF se Text nikalna (The Eyes) ---
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        # Har page ko padh ke text variable mein jodte jao
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# --- Function 2: AI se Risk Analysis karwana (The Brain) ---
def analyze_clause_with_llm(clause_text):
    # Ye hai humara "Prompt Design" - AI ko instruction dena
    template = """
    You are an expert Legal Risk Analyzer for Indian Contracts. 
    Analyze the following contract text strictly.
    
    Identify key clauses that might be risky for the user (like Data Privacy, Termination, Indemnity).
    
    For each identified risk, provide:
    1. Clause Name
    2. Risk Level (High/Medium/Low)
    3. Simple Explanation (Why is it risky?)
    
    Input Text:
    {text}
    
    Output Format (Keep it concise and bulleted):
    """
    
    prompt = PromptTemplate(template=template, input_variables=["text"])
    
    # Chain banana (Prompt + Model ek saath)
    chain = prompt | llm
    
    # AI ko run karna
    response = chain.invoke({"text": clause_text})
    
    return response.content