import streamlit as st
from utils import get_pdf_text, analyze_clause_with_llm

# --- Page Setup (Tab ka naam aur icon) ---
st.set_page_config(page_title="Legal Risk Analyzer", page_icon="⚖️", layout="wide")

# --- Custom CSS (Ye hai wo "Shandaar" look ka raaz) ---
st.markdown("""
    <style>
    .main {
        background-color: #0E1117; 
        color: #FAFAFA;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B; 
        color: white; 
        font-weight: bold;
    }
    .header-box {
        padding: 20px;
        background-color: #262730;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    /* Risk Cards Styling */
    .risk-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #808080; /* Default Grey */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    .risk-high { border-left: 5px solid #FF4B4B; }   /* Red */
    .risk-medium { border-left: 5px solid #FFA726; } /* Orange */
    .risk-low { border-left: 5px solid #66BB6A; }    /* Green */
    
    .card-title { font-size: 18px; font-weight: bold; color: #FFFFFF; }
    .card-badge { 
        display: inline-block; 
        padding: 2px 8px; 
        border-radius: 4px; 
        font-size: 12px; 
        font-weight: bold; 
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="header-box"><h1>⚖️ Legal Risk & Clause Analyzer</h1><p>Upload a contract to identify hidden risks automatically using AI.</p></div>', unsafe_allow_html=True)

# --- Sidebar (Control Panel) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4252/4252336.png", width=100)
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload Contract (PDF)", type="pdf")
    
    st.markdown("---")
    st.markdown("### 🧠 How it works")
    st.info("1. AI reads the PDF.\n2. Extracts legal clauses.\n3. Flags High/Medium risks.")
    st.markdown("---")
    st.caption("Project by Siddhant")

# --- Main App Logic ---
if uploaded_file is not None:
    st.success("✅ File Uploaded! Click below to analyze.")
    
    if st.button("🚀 Analyze Risks Now"):
        with st.spinner("🕵️ AI is reading the contract... (This may take 10-20 seconds)"):
            
            # 1. Text Extraction
            text = get_pdf_text([uploaded_file])
            
            # 2. AI Analysis (Limit to 10k chars to save quota)
            raw_analysis = analyze_clause_with_llm(text[:15000])
            
            # --- Result Display Logic ---
            st.markdown("## 📊 Analysis Report")
            
            # Hum AI ke text ko split karke cards banayenge
            # AI usually "**Clause Name:**" format use kar raha hai
            clauses = raw_analysis.split("**Clause Name:**")
            
            # Pehla part usually empty hota hai split ke baad, usse skip karte hain
            for clause in clauses[1:]:
                # Logic to determine color based on risk keywords
                risk_color = "risk-low"
                badge_color = "#66BB6A" # Green
                risk_label = "LOW RISK"
                
                if "High" in clause or "Risk Level:** High" in clause:
                    risk_color = "risk-high"
                    badge_color = "#FF4B4B" # Red
                    risk_label = "HIGH RISK"
                elif "Medium" in clause or "Risk Level:** Medium" in clause:
                    risk_color = "risk-medium"
                    badge_color = "#FFA726" # Orange
                    risk_label = "MEDIUM RISK"

                # HTML Card Render karna
                st.markdown(f"""
                <div class="risk-card {risk_color}">
                    <span class="card-badge" style="background-color: {badge_color}; color: white;">{risk_label}</span>
                    <div class="card-title">Clause: {clause.split('**')[0]}</div>
                    <p style="color: #CCCCCC;">{clause}</p>
                </div>
                """, unsafe_allow_html=True)

else:
    # Empty State (Jab kuch upload nahi kiya)
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; color: #666;'>
        <h3>👈 Upload a PDF from the sidebar to start</h3>
        <p>Supports: Employment Contracts, NDAs, Rental Agreements</p>
    </div>
    """, unsafe_allow_html=True)