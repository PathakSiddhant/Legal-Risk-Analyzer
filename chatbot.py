import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- GEMINI MODEL ---
chat_model = ChatGoogleGenerativeAI(
    model="gemini-flash-latest", 
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

def get_chat_response(question, contract_text, analysis_summary, chat_history):
    """
    Smarter Chatbot that knows the Dashboard Analysis.
    """
    
    template = """
    You are LexiSafe, an intelligent legal assistant.
    
    1. THE CONTRACT TEXT:
    {context}
    
    2. RISKS ALREADY DETECTED BY SYSTEM (Dashboard Data):
    {analysis_summary}
    
    3. CONVERSATION HISTORY:
    {history}
    
    USER QUESTION:
    {question}
    
    INSTRUCTIONS:
    - Your main job is to explain the contract and the risks mentioned in the 'Dashboard Data'.
    - If the user asks about risks, REFER to the "Dashboard Data" provided above.
    - Do not contradict the system's analysis.
    - Keep answers short, professional, and easy to understand.
    """
    
    prompt = PromptTemplate(
        input_variables=["context", "analysis_summary", "history", "question"],
        template=template
    )
    
    chain = prompt | chat_model | StrOutputParser()
    
    try:
        response = chain.invoke({
            "context": contract_text,
            "analysis_summary": analysis_summary,
            "history": chat_history,
            "question": question
        })
        return response
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"