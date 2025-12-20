import streamlit as st
from utils import get_pdf_text, analyze_clause_with_llm

st.set_page_config(page_title="Legal Risk Analyzer", page_icon="⚖️", layout="wide")

# --- Custom CSS (Cluster Styling) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FAFAFA; }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
    
    /* Risk Cards inside Expanders */
    .risk-card {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: #1E1E1E;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .high-border { border-left: 5px solid #FF4B4B; }
    .medium-border { border-left: 5px solid #FFA726; }
    .low-border { border-left: 5px solid #66BB6A; }
    
    .clause-title { font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    .clause-risk { font-weight: bold; font-size: 14px; }
    .clause-desc { color: #CCCCCC; font-size: 14px; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("⚖️ Legal Risk Analyzer")
st.markdown("### 🛡️ Contract Review Dashboard")

# --- Sidebar ---
with st.sidebar:
    st.header("📂 Upload Document")
    uploaded_file = st.file_uploader("Upload Contract (PDF)", type="pdf")
    st.info("Analysis Focus: \n- 🔴 High Risks (Must Fix)\n- 🟡 Medium Risks (Negotiable)\n- 🟢 Safe Clauses")

# --- Main Logic ---
if uploaded_file is not None:
    # 1. Store state to avoid reload (Session State)
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
        st.session_state.risks = {"High": [], "Medium": [], "Low": []}

    # Analyze Button
    if st.button("🚀 Analyze Contract"):
        with st.spinner("🔍 AI is creating the Risk Dashboard..."):
            text = get_pdf_text([uploaded_file])
            raw_analysis = analyze_clause_with_llm(text[:20000]) # Limit increased
            
            # --- Parsing Logic (Convert Text to Data) ---
            # Hum '###' se tod kar list banayenge
            clauses = raw_analysis.split("###")
            
            # Reset lists
            high_risks = []
            medium_risks = []
            low_risks = []
            
            for clause in clauses:
                if "|" in clause: # Check valid format
                    try:
                        parts = clause.split("|")
                        title = parts[0].strip()
                        risk = parts[1].strip()
                        explanation = parts[2].strip()
                        
                        data = {"title": title, "explanation": explanation}
                        
                        if "High" in risk:
                            high_risks.append(data)
                        elif "Medium" in risk:
                            medium_risks.append(data)
                        else:
                            low_risks.append(data)
                    except:
                        continue # Skip bad formatting
            
            # Save to session state
            st.session_state.risks["High"] = high_risks
            st.session_state.risks["Medium"] = medium_risks
            st.session_state.risks["Low"] = low_risks
            st.session_state.analysis_done = True

    # --- Display Dashboard (Only if analysis is done) ---
    if st.session_state.analysis_done:
        st.markdown("---")
        
        # 1. The Big Numbers (Cluster View)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="🔴 High Risks", value=len(st.session_state.risks["High"]))
        with col2:
            st.metric(label="🟡 Medium Risks", value=len(st.session_state.risks["Medium"]))
        with col3:
            st.metric(label="🟢 Low Risks", value=len(st.session_state.risks["Low"]))
            
        st.markdown("---")
        
        # 2. Detailed Expanders (Click to Open)
        
        # --- HIGH RISK SECTION ---
        with st.expander("🔴 View High Risk Clauses", expanded=True): # Default open
            if len(st.session_state.risks["High"]) > 0:
                for item in st.session_state.risks["High"]:
                    st.markdown(f"""
                    <div class="risk-card high-border">
                        <div class="clause-title">{item['title']}</div>
                        <div class="clause-desc">{item['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("No High Risks found! 🎉")

        # --- MEDIUM RISK SECTION ---
        with st.expander("🟡 View Medium Risk Clauses", expanded=False):
            if len(st.session_state.risks["Medium"]) > 0:
                for item in st.session_state.risks["Medium"]:
                    st.markdown(f"""
                    <div class="risk-card medium-border">
                        <div class="clause-title">{item['title']}</div>
                        <div class="clause-desc">{item['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No Medium Risks found.")

        # --- LOW RISK SECTION ---
        with st.expander("🟢 View Low Risk Clauses", expanded=False):
            if len(st.session_state.risks["Low"]) > 0:
                for item in st.session_state.risks["Low"]:
                    st.markdown(f"""
                    <div class="risk-card low-border">
                        <div class="clause-title">{item['title']}</div>
                        <div class="clause-desc">{item['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No Low Risks found.")

else:
    st.markdown("<br><br><h3 style='text-align: center;'>👈 Upload a PDF to see the Magic Dashboard</h3>", unsafe_allow_html=True)