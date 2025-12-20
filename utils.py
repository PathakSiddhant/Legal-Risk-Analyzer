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
    template = """
    You are an expert Legal Risk Analyzer. 
    Analyze the contract text and identify risky clauses.
    
    OUTPUT FORMAT INSTRUCTIONS (STRICTLY FOLLOW THIS):
    1. Separate each clause with "###"
    2. Within each clause, separate Title, Risk, and Explanation with "|"
    3. Format: Clause Name | Risk Level (High/Medium/Low) | Explanation (Bullet points)
    4. Do not add any intro/outro text.
    
    Example Output:
    Unilateral Termination | High | The company can fire you without notice.
    ###
    Data Selling | High | Your data is sold to 3rd parties.
    ###
    Jurisdiction | Low | Standard court clauses.

    Input Text:
    {text}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm
    response = chain.invoke({"text": clause_text})
    
    # Handle List vs String output (Gemini Quirk Fix)
    if isinstance(response.content, list):
        final_text = ""
        for item in response.content:
            if isinstance(item, dict) and 'text' in item:
                final_text += item['text']
        return final_text
    else:
        return response.content
    