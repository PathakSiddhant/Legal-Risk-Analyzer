import streamlit as st
import time
from utils import get_pdf_text, analyze_clause_with_llm
from chatbot import get_chat_response

# --- Page Config ---
st.set_page_config(page_title="LexiSafe AI", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# --- CSS STYLING (ANIMATIONS RESTORED) ---
st.markdown("""
    <style>
    /* 1. FONTS & BACKGROUND */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* 2. HERO TITLE */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        text-align: center; color: #AAA; font-size: 1.2rem; margin-bottom: 40px;
    }

    /* 3. LANDING FEATURE CARDS (ANIMATION FIXED 🚀) */
    .feature-card {
        background-color: #161B22;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #30363D;
        text-align: center;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Smooth Bouncy Effect */
        position: relative;
        overflow: hidden;
    }
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02); /* Lift Up & Zoom */
        border-color: #00C9FF;
        box-shadow: 0 15px 30px rgba(0, 201, 255, 0.15); /* Neon Glow Shadow */
        background-color: #1A1F2E;
    }
    .feature-icon { font-size: 35px; margin-bottom: 15px; transition: 0.3s; }
    .feature-card:hover .feature-icon { transform: scale(1.2); } /* Icon Pop */
    
    .feature-title { font-size: 1.2rem; font-weight: 700; color: white; margin-bottom: 8px; }
    .feature-desc { font-size: 0.95rem; color: #8B949E; line-height: 1.5; }

    /* 4. METRIC BOXES */
    .metric-container { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }
    .metric-box {
        background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 20px; text-align: center; width: 100%; transition: transform 0.2s;
    }
    .metric-box:hover { transform: translateY(-5px); border-color: #58A6FF; }
    .metric-number { font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; }
    .metric-label { font-size: 0.9rem; color: #8B949E; text-transform: uppercase; letter-spacing: 1px; }

    .metric-red { border-top: 4px solid #FF4B4B; } .num-red { color: #FF4B4B; }
    .metric-yellow { border-top: 4px solid #FFA726; } .num-yellow { color: #FFA726; }
    .metric-green { border-top: 4px solid #00C9FF; } .num-green { color: #00C9FF; }

    /* 5. RISK CARDS */
    .risk-card {
        background-color: #161B22; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #30363D; transition: transform 0.2s ease;
    }
    .high-border { border-left: 4px solid #FF4B4B; }
    .high-border:hover { border-color: #FF4B4B; transform: translateY(-3px); }
    .medium-border { border-left: 4px solid #FFA726; }
    .medium-border:hover { border-color: #FFA726; transform: translateY(-3px); }
    .low-border { border-left: 4px solid #00C9FF; }
    .low-border:hover { border-color: #00C9FF; transform: translateY(-3px); }

    .card-title { font-size: 1.1rem; font-weight: 700; color: #FFF; margin-bottom: 5px; }
    .card-fix { margin-top: 12px; background: rgba(56, 139, 253, 0.1); padding: 10px; border-radius: 6px; font-size: 0.95rem; color: #58A6FF; border-left: 3px solid #58A6FF; }

    /* 6. STATUS CARD */
    .status-card { background: #12141C; border: 1px solid #30363D; border-radius: 8px; padding: 15px; margin-top: 10px; }
    .status-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px; color: #C9D1D9; }
    .blink { width: 8px; height: 8px; background-color: #00F260; border-radius: 50%; display: inline-block; box-shadow: 0 0 5px #00F260; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    
    /* 7. FOOTER */
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0E1117; color: #8B949E; text-align: center; padding: 20px; font-size: 15px; border-top: 1px solid #30363D; z-index: 1000; }
    .footer a { color: #58A6FF; text-decoration: none; font-weight: bold; }
    
    /* 8. BUTTONS */
    .stButton>button { background-color: #238636; color: white; font-weight: 600; border: 1px solid rgba(255,255,255,0.1); padding: 12px 24px; border-radius: 6px; width: 100%; }
    
    #MainMenu {visibility: visible;} footer {visibility: hidden;} header {visibility: visible;} .block-container { padding-bottom: 80px; }
    </style>
""", unsafe_allow_html=True)

# --- CACHING ---
@st.cache_data(show_spinner=False)
def get_pdf_text_cached(f): return get_pdf_text([f])
@st.cache_data(show_spinner=False)
def analyze_clause_cached(t): return analyze_clause_with_llm(t)

# --- SESSION STATE ---
if 'last_file' not in st.session_state: st.session_state.last_file = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = ""
if 'messages' not in st.session_state: st.session_state.messages = []
if 'chat_open' not in st.session_state: st.session_state.chat_open = False

# --- DIALOG FUNCTION ---
@st.dialog("💬 LexiSafe Assistant", width="large")
def open_chat_modal(pdf_text, analysis_summary):
    st.markdown("Ask specific questions about your contract clauses, risks, or terms.")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Ex: What is the notice period for termination?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing contract..."):
                reply = get_chat_response(prompt, pdf_text, analysis_summary, st.session_state.chat_history)
                st.markdown(reply)
        
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.chat_history += f"\nUser: {prompt}\nAI: {reply}"
        st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;"><span style="font-size: 26px;">⚖️</span><div><div style="font-size: 20px; font-weight: 700; color: #FFF; line-height: 1;">LexiSafe</div><div style="font-size: 11px; color: #8B949E;">Contract AI v1.0</div></div></div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📄 Upload Contract")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""<div style="font-size: 12px; font-weight: 700; color: #8B949E; margin-bottom: 5px;">SYSTEM STATUS</div><div class="status-card"><div class="status-row"><span>Server</span><span><span class="blink"></span> &nbsp; Online</span></div><div class="status-row"><span>Model</span><span style="color: #58A6FF;">Gemini 2.0</span></div></div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CHAT BUTTON
    if uploaded_file and st.session_state.get("analysis_done", False):
        if st.button("💬 Chat with AI Assistant", type="secondary", use_container_width=True):
            st.session_state.chat_open = True
            st.rerun()

# --- MAIN LOGIC ---
if uploaded_file and st.session_state.last_file != uploaded_file.name:
    st.session_state.analysis_done = False
    st.session_state.risks = {"High": [], "Medium": [], "Low": []}
    st.session_state.messages = []
    st.session_state.chat_history = ""
    st.session_state.chat_open = False
    st.session_state.last_file = uploaded_file.name
    st.rerun()

# 1. LANDING
if not uploaded_file:
    st.markdown('<br><div class="hero-title">Legal Risk Analyzer</div><div class="hero-subtitle">Upload a contract. Detect risks. Protect your business.</div>', unsafe_allow_html=True)
    
    # --- RESTORED ANIMATED CARDS ---
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="feature-card"><div class="feature-icon">🚀</div><div class="feature-title">Instant Analysis</div><div class="feature-desc">Full contract review in seconds.</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feature-card"><div class="feature-icon">🔍</div><div class="feature-title">Risk Detection</div><div class="feature-desc">AI finds hidden liabilities.</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="feature-card"><div class="feature-icon">🛡️</div><div class="feature-title">Legal Shield</div><div class="feature-desc">Smart fixes for safer terms.</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 **Upload your PDF from the sidebar to begin.**")

# 2. ANALYSIS
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

    # 3. DASHBOARD
    if st.session_state.analysis_done:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        h, m, l = len(st.session_state.risks["High"]), len(st.session_state.risks["Medium"]), len(st.session_state.risks["Low"])
        
        with c1: st.markdown(f'<div class="metric-box metric-red"><div class="metric-number num-red">{h}</div><div class="metric-label">Critical Risks</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-box metric-yellow"><div class="metric-number num-yellow">{m}</div><div class="metric-label">Warnings</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-box metric-green"><div class="metric-number num-green">{l}</div><div class="metric-label">Safe Clauses</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
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

# --- CHAT OPEN LOGIC ---
if st.session_state.chat_open:
    text_context = get_pdf_text_cached(uploaded_file)
    risk_summary = f"High: {len(st.session_state.risks['High'])}, Med: {len(st.session_state.risks['Medium'])}.\n"
    if st.session_state.risks['High']:
        risk_summary += "Critical:\n" + "\n".join([f"- {r['title']}: {r['expl']}" for r in st.session_state.risks['High']])
    open_chat_modal(text_context, risk_summary)

# --- FOOTER ---
st.markdown("""<div class="footer">Designed by <a href="https://github.com/TeraUsername" target="_blank">Siddhant</a> | Powered by Gemini 2.0</div>""", unsafe_allow_html=True)