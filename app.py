import streamlit as st
import time
from utils import get_pdf_text, analyze_clause_with_llm
from chatbot import get_chat_response
from report_generator import create_pdf_report
from email_generator import generate_email

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="LexiSafe AI", 
    page_icon="⚖️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS STYLING (ANIMATIONS RESTORED 🎨)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* --- HERO SECTION --- */
    .hero-container {
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 3.5rem; 
        font-weight: 800;
        background: linear-gradient(120deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    .hero-subtitle { 
        color: #C9D1D9; 
        font-size: 1.2rem; 
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
        opacity: 0.8;
    }

    /* --- ANIMATED FEATURE CARDS --- */
    .feature-card { 
        background-color: #161B22; 
        padding: 30px; 
        border-radius: 16px; 
        border: 1px solid #30363D; 
        text-align: center; 
        height: 100%; 
        transition: all 0.3s ease-in-out; /* Enable Animation */
        position: relative;
        overflow: hidden;
    }
    
    /* HOVER EFFECT (The Animation) */
    .feature-card:hover { 
        transform: translateY(-10px); 
        border-color: #00C9FF; 
        background-color: #1A1F2E;
        box-shadow: 0 10px 30px rgba(0, 201, 255, 0.1); 
    }
    .feature-icon { font-size: 35px; margin-bottom: 15px; }

    /* --- ANIMATED METRIC BOXES --- */
    .metric-box { 
        background-color: #161B22; 
        border: 1px solid #30363D; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center; 
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .metric-box:hover { 
        transform: translateY(-5px); 
        border-color: #58A6FF; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .metric-number { font-size: 2.2rem; font-weight: 800; }
    .metric-label { font-size: 0.8rem; color: #8B949E; text-transform: uppercase; }
    
    .metric-red { border-top: 4px solid #FF4B4B; } .num-red { color: #FF4B4B; }
    .metric-yellow { border-top: 4px solid #FFA726; } .num-yellow { color: #FFA726; }
    .metric-green { border-top: 4px solid #00C9FF; } .num-green { color: #00C9FF; }

    /* --- ANIMATED RISK CARDS --- */
    .risk-card { 
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 15px; 
        border: 1px solid #30363D; 
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .risk-card:hover { 
        transform: translateX(5px); 
        background-color: #1c2128;
    }
    
    .high-border { border-left: 4px solid #FF4B4B; }
    .medium-border { border-left: 4px solid #FFA726; }
    .low-border { border-left: 4px solid #00C9FF; }

    .card-title { font-size: 1.1rem; font-weight: 700; color: #FFF; margin-bottom: 5px; }
    .card-fix { margin-top: 12px; background: rgba(56, 139, 253, 0.1); padding: 10px; border-radius: 6px; color: #58A6FF; border-left: 3px solid #58A6FF; }

    /* --- UI ELEMENTS --- */
    .dialog-header {
        background: linear-gradient(90deg, #1F6FEB 0%, #0D1117 100%);
        padding: 15px; border-radius: 8px; margin-bottom: 20px;
        display: flex; align-items: center; gap: 10px; border-bottom: 2px solid #58A6FF;
    }
    .dialog-title { font-size: 18px; font-weight: 700; color: white; margin: 0; }
    
    .email-container { background-color: #0D1117; border: 1px solid #30363D; border-radius: 8px; padding: 20px; margin-top: 15px; }
    .email-label { color: #8B949E; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0E1117; color: #8B949E; text-align: center; padding: 12px; font-size: 13px; border-top: 1px solid #30363D; z-index: 9999; }
    .stButton>button { background-color: #238636; color: white; font-weight: 600; border: 1px solid rgba(255,255,255,0.1); padding: 12px 24px; border-radius: 6px; width: 100%; }
    
    /* TOOLKIT EXPANDER */
    .streamlit-expanderHeader { font-weight: 600; background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; }

    #MainMenu {visibility: visible;} footer {visibility: hidden;} header {visibility: visible;} 
    .block-container { padding-bottom: 80px; }
    
    /* --- FOOTER --- */
    .footer { 
        position: fixed; 
        left: 0; 
        bottom: 0; 
        width: 100%; 
        background-color: #0E1117; 
        color: #8B949E; 
        text-align: center; 
        padding: 15px; 
        font-size: 13px; 
        border-top: 1px solid #30363D; 
        z-index: 100; 
    }
    
    .footer a { 
        color: #58A6FF; 
        text-decoration: none; 
        font-weight: 600; 
        transition: 0.3s; 
    }
    
    .footer a:hover { 
        color: #00C9FF; 
        text-shadow: 0 0 5px rgba(0, 201, 255, 0.5); 
    }
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
@st.cache_data(show_spinner=False)
def get_pdf_text_cached(f): return get_pdf_text(f)

@st.cache_data(show_spinner=False)
def analyze_clause_cached(t): return analyze_clause_with_llm(t)

def set_modal_chat(): st.session_state.active_modal = "chat"
def set_modal_email(): st.session_state.active_modal = "email"
def close_modals(): st.session_state.active_modal = None

# ==========================================
# 4. SESSION STATE
# ==========================================
if 'last_file' not in st.session_state: st.session_state.last_file = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = ""
if 'messages' not in st.session_state: st.session_state.messages = []
if 'active_modal' not in st.session_state: st.session_state.active_modal = None 
if 'risks' not in st.session_state: st.session_state.risks = {"High": [], "Medium": [], "Low": []}
if 'email_draft' not in st.session_state: st.session_state.email_draft = "" 

# ==========================================
# 5. ENHANCED DIALOGS
# ==========================================

# --- A. CHATBOT DIALOG ---
@st.dialog("💬 LexiSafe Assistant", width="large")
def open_chat_modal(pdf_text, analysis_summary):
    st.markdown("""
        <div class="dialog-header">
            <span style="font-size: 24px;">🤖</span>
            <span class="dialog-title">Contract Assistant</span>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Ask about clauses, dates, or risks..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing contract context..."):
                reply = get_chat_response(prompt, pdf_text, analysis_summary, st.session_state.chat_history)
                st.markdown(reply)
        
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.chat_history += f"\nUser: {prompt}\nAI: {reply}"
        st.rerun()

# --- B. EMAIL GENERATOR DIALOG ---
@st.dialog("📧 Negotiation Drafter", width="large")
def open_email_modal(filename, risks):
    st.markdown("""
        <div class="dialog-header">
            <span style="font-size: 24px;">✍️</span>
            <span class="dialog-title">Email Architect</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Target:** Drafting negotiation email for `{filename}`")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✨ Draft Now", key="gen_email_btn", use_container_width=True):
            with st.spinner("Crafting legal response..."):
                email_content = generate_email(filename, risks)
                st.session_state.email_draft = email_content
                st.rerun()
    
    if st.session_state.email_draft:
        st.markdown("<div class='email-container'>", unsafe_allow_html=True)
        st.markdown("<div class='email-label'>Subject Line</div>", unsafe_allow_html=True)
        st.info("Contract Review: Proposed Adjustments for Approval")
        
        st.markdown("<div class='email-label' style='margin-top:15px;'>Email Body</div>", unsafe_allow_html=True)
        st.text_area("Content", value=st.session_state.email_draft, height=350, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("💡 Pro Tip: Review the draft and copy it to your email client.")

# ==========================================
# 6. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;"><span style="font-size: 26px;">⚖️</span><div><div style="font-size: 20px; font-weight: 700; color: #FFF; line-height: 1;">LexiSafe</div><div style="font-size: 11px; color: #8B949E;">Contract AI v1.0</div></div></div>""", unsafe_allow_html=True)
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    
    # Tool Kit (Hidden until analysis is done)
    if uploaded_file and st.session_state.get("analysis_done", False):
        st.markdown("---")
        with st.expander("🛠️ **Professional Toolkit**", expanded=True):
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
            if st.button("💬 &nbsp; AI Chat Assistant", use_container_width=True, on_click=set_modal_chat): pass 
            if st.button("📧 &nbsp; Email Drafter", use_container_width=True, on_click=set_modal_email): pass
            
            pdf_bytes = create_pdf_report(uploaded_file.name, st.session_state.risks)
            st.download_button(
                label="📄 &nbsp; Export PDF Report",
                data=pdf_bytes,
                file_name="LexiSafe_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                on_click=close_modals
            )

# ==========================================
# 7. MAIN LOGIC
# ==========================================
if uploaded_file and st.session_state.last_file != uploaded_file.name:
    st.session_state.analysis_done = False
    st.session_state.risks = {"High": [], "Medium": [], "Low": []}
    st.session_state.messages = []
    st.session_state.chat_history = ""
    st.session_state.email_draft = ""
    st.session_state.active_modal = None 
    st.session_state.last_file = uploaded_file.name
    st.rerun()

if not uploaded_file:
    # HERO SECTION (Centered & Professional)
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Legal Risk Analyzer</div>
            <div class="hero-subtitle">Upload a contract. Detect risks. Protect your business.</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="feature-card"><div class="feature-icon">🚀</div><div class="feature-title">Instant Analysis</div><div class="feature-desc">Full contract review in seconds.</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feature-card"><div class="feature-icon">🔍</div><div class="feature-title">Risk Detection</div><div class="feature-desc">AI finds hidden liabilities.</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="feature-card"><div class="feature-icon">🛡️</div><div class="feature-title">Legal Shield</div><div class="feature-desc">Smart fixes for safer terms.</div></div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 **Upload your PDF from the sidebar to begin.**")

else:
    st.markdown(f"### 📑 Analysis Report: `{uploaded_file.name}`")
    
    if not st.session_state.analysis_done:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 RUN RISK ASSESSMENT"):
            with st.spinner("🧠 Scanning document layers..."):
                text = get_pdf_text_cached(uploaded_file)
                raw = analyze_clause_cached(text[:25000])
                clauses = raw.split("###")
                st.session_state.risks = {"High": [], "Medium": [], "Low": []}
                for c in clauses:
                    if "|" in c:
                        try:
                            p = c.split("|")
                            if len(p) >= 3:
                                d = {"title": p[0].strip(), "risk": p[1].strip(), "expl": p[2].strip(), "fix": p[3].strip() if len(p)>3 else ""}
                                if "High" in d["risk"]: st.session_state.risks["High"].append(d)
                                elif "Medium" in d["risk"]: st.session_state.risks["Medium"].append(d)
                                else: st.session_state.risks["Low"].append(d)
                        except: continue
                st.session_state.analysis_done = True
                st.rerun()

    if st.session_state.analysis_done:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Metrics with Hover Animation
        c1, c2, c3 = st.columns(3)
        h, m, l = len(st.session_state.risks["High"]), len(st.session_state.risks["Medium"]), len(st.session_state.risks["Low"])
        with c1: st.markdown(f'<div class="metric-box metric-red"><div class="metric-number num-red">{h}</div><div class="metric-label">Critical Risks</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-box metric-yellow"><div class="metric-number num-yellow">{m}</div><div class="metric-label">Warnings</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-box metric-green"><div class="metric-number num-green">{l}</div><div class="metric-label">Safe Clauses</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk Lists
        t1, t2, t3 = st.tabs(["🔥 Critical", "⚠️ Warnings", "✅ Safe"])
        def render_list(risk_type, border_cls):
            items = st.session_state.risks[risk_type]
            if not items: st.markdown(f"<div style='text-align:center; padding:20px; color:#666;'>No {risk_type} risks found.</div>", unsafe_allow_html=True); return
            for item in items: st.markdown(f'<div class="risk-card {border_cls}"><div class="card-title">{item["title"]}</div><div style="color: #C9D1D9; font-size: 0.95rem; margin-bottom: 10px;">{item["expl"]}</div><div class="card-fix">💡 <b>Fix:</b> {item["fix"]}</div></div>', unsafe_allow_html=True)

        with t1: render_list("High", "high-border")
        with t2: render_list("Medium", "medium-border")
        with t3: render_list("Low", "low-border")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Check Another File"):
            st.session_state.last_file = None
            st.rerun()

# --- TRIGGER: MODALS ---
if st.session_state.active_modal == 'chat':
    text_context = get_pdf_text_cached(uploaded_file)
    risk_summary = f"High: {len(st.session_state.risks['High'])}, Med: {len(st.session_state.risks['Medium'])}."
    if st.session_state.risks['High']:
        risk_summary += "Critical:\n" + "\n".join([f"- {r['title']}: {r['expl']}" for r in st.session_state.risks['High']])
    open_chat_modal(text_context, risk_summary)

elif st.session_state.active_modal == 'email':
    open_email_modal(uploaded_file.name, st.session_state.risks)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        <span>🛡️ <b>LexiSafe AI</b> &nbsp;•&nbsp; Intelligent Contract Security</span>
        &nbsp;&nbsp;<span style="color: #30363D;">|</span>&nbsp;&nbsp;
        <span>Developed by <a href="https://github.com/PathakSiddhant" target="_blank">Siddhant Pathak</a></span>
    </div>
""", unsafe_allow_html=True)