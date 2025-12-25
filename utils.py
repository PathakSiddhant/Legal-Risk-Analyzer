import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- MODEL (Fixed Name) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

def get_pdf_text(uploaded_file):
    """
    Extracts text from a single PDF file using pypdf.
    """
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def analyze_clause_with_llm(clause_text):
    """
    Analyzes the contract text using Gemini.
    """
    template = """
    You are an expert legal AI. Analyze the following contract text and identify risks.
    
    Output format must be strictly:
    Clause Title | Risk Level (High/Medium/Low) | Brief Explanation | Recommendation/Fix
    ###
    
    Rules:
    1. Separate each risk with "###".
    2. Use "|" as a delimiter.
    3. Be concise.
    4. If text is empty or unreadable, say "No Content Found".
    
    Contract Text:
    {text}
    """
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({"text": clause_text})
        return response
    except Exception as e:
        return f"Error: {str(e)}"