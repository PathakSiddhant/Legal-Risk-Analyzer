import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- GEMINI MODEL ---
# FIX: Removed '-latest' which was causing the 404 Error
email_model = ChatGoogleGenerativeAI(
    model="gemini-flash-latest", 
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7 
)

def generate_email(contract_name, risks):
    """
    Generates a professional negotiation email based on detected risks.
    """
    
    risk_summary = ""
    for r in risks['High']:
        risk_summary += f"- Critical Issue: {r['title']}. Reason: {r['expl']}. Proposed Fix: {r['fix']}\n"
    for r in risks['Medium']:
        risk_summary += f"- Concern: {r['title']}. Reason: {r['expl']}. Proposed Fix: {r['fix']}\n"

    if not risk_summary:
        return "Subject: Contract Review - Ready to Sign\n\nDear Team,\n\nWe have reviewed the contract and found no significant risks. We are ready to proceed.\n\nBest regards,\n[Your Name]"

    template = """
    You are a professional corporate lawyer representing a client.
    Your task is to draft a polite but firm negotiation email to the counterparty regarding the contract: "{contract_name}".

    The following risks/issues were identified in the contract:
    {risks}

    INSTRUCTIONS:
    - Subject Line: Professional and clear.
    - Tone: Collaborative, professional, yet firm on protecting interests.
    - Structure: 
      1. Opening (referencing the contract review).
      2. The "Ask" (list the clauses that need changes and briefly explain why, using the Proposed Fixes).
      3. Closing (looking forward to finalizing).
    - Do not use placeholders like [Your Name], just keep it generic like "Legal Team".
    """

    prompt = PromptTemplate(
        input_variables=["contract_name", "risks"],
        template=template
    )

    chain = prompt | email_model | StrOutputParser()

    try:
        return chain.invoke({
            "contract_name": contract_name,
            "risks": risk_summary
        })
    except Exception as e:
        return f"Error generating email: {str(e)}"