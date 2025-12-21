import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

# --- CHANGE IS HERE: Temperature = 0.0 (Zero Creativity, 100% Consistency) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.0 
)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def analyze_clause_with_llm(clause_text):
    template = """
    You are an expert Legal Risk Analyzer. 
    Analyze the contract text and identify risky clauses.
    
    OUTPUT FORMAT INSTRUCTIONS (STRICTLY FOLLOW THIS):
    1. Separate each clause with "###"
    2. Within each clause, separate Title, Risk, Explanation, and Recommendation with "|"
    3. Format: Clause Name | Risk Level (High/Medium/Low) | Explanation (Why is it bad?) | Recommendation (How to fix it?)
    4. Do not add any intro/outro text.
    
    Example Output:
    Unilateral Termination | High | The company can fire you without notice. | Negotiate for at least 30 days notice period.
    ###
    Data Selling | High | Your data is sold to 3rd parties. | Ask to remove this clause or limit data usage.
    ###
    Jurisdiction | Low | Standard court clauses. | No action needed.

    Input Text:
    {text}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm
    response = chain.invoke({"text": clause_text})
    
    if isinstance(response.content, list):
        final_text = ""
        for item in response.content:
            if isinstance(item, dict) and 'text' in item:
                final_text += item['text']
        return final_text
    else:
        return response.content