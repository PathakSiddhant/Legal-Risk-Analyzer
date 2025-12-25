# 🛡️ LexiSafe AI — Intelligent Contract Risk Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Gemini AI](https://img.shields.io/badge/Powered%20By-Google%20Gemini-orange?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**LexiSafe AI** is a next-generation AI-powered legal contract analysis platform that instantly detects risks, explains complex clauses, and helps users negotiate better.

---

## 🚀 What is LexiSafe AI?

LexiSafe AI helps individuals, startups, and businesses understand hidden legal risks inside long and complex contracts without requiring any legal expertise.

**Upload a contract → Get instant insights → Take action with confidence.**

---

## ✨ Key Features

### 🔍 **Intelligent Risk Detection**
* **🔥 Critical Risks:** Identifies clauses that pose significant liability.
* **⚠️ Warnings:** Highlights unfavorable or ambiguous terms.
* **✅ Safe Clauses:** Confirms standard and safe terms.
* **🧠 Simple Explanations:** Translates legal jargon into plain English.

### 💬 **AI Legal Assistant (Chat with Your Contract)**
Ask specific questions about your document, such as:
* *"What is the termination notice period?"*
* *"Is there a non-compete clause?"*
* *"What penalties exist for a breach?"*

### 📧 **Negotiation Email Generator**
* One-click generation of professional negotiation emails.
* Content is strictly based on the detected risks.
* Ready to copy-paste and send.

### 📄 **Downloadable Risk Report**
* Export a comprehensive PDF report.
* Includes clause-by-clause breakdown, severity levels, and actionable recommendations.

### 🎨 **Premium User Experience**
* **🌙 Dark Mode:** Sleek interface designed for focus.
* **⚡ Fast & Smooth:** Animated interactions for a premium feel.
* **🔒 Privacy-First:** Documents are processed in-memory and **never stored**.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **AI Model** | Google Gemini 1.5 Flash |
| **LLM Framework** | LangChain |
| **PDF Processing** | PyPDF, PDFPlumber |
| **Report Generation** | FPDF |
| **Configuration** | Python-Dotenv |

---

## ⚙️ Installation & Local Setup

Follow these steps to run LexiSafe AI locally:

### ⚡ Quickstart
Prerequisites: Python 3.9+ and Git

1) Clone the repository
```bash
git clone https://github.com/PathakSiddhant/Legal-Risk-Analyzer.git
cd Legal-Risk-Analyzer
```

2) (Recommended) Create and activate a virtual environment
```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS / Linux
# source venv/bin/activate
```

3) Install dependencies
```bash
pip install -r requirements.txt
```

4) Configure API key (see 'Configuration' section), then run the app:
```bash
streamlit run app.py
```

Open the UI at the URL shown by Streamlit (usually http://localhost:8501).

---

## Configuration
This project expects a Google API key set in environment variables. Create a `.env` file in the project root with:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Notes:
- Do **not** commit your `.env` file or API keys to GitHub. `.gitignore` already includes `.env`.
- The code reads `GOOGLE_API_KEY` in modules such as `chatbot.py`, `diagnose.py`, `utils.py`, and `email_generator.py`.

---

## Usage
- Upload a contract (PDF or text) via the web UI
- Review detected clause risks and suggested actions
- Use the chat to ask specific questions about clauses
- Generate negotiation emails using the email generator
- Download a full risk report (PDF)

---

## Directory Structure

```text
Legal-Risk-Analyzer/
├── app.py                  # Main Streamlit Application
├── chatbot.py              # Logic for AI Chat Assistant
├── email_generator.py      # Logic for Negotiation Email drafting
├── utils.py                # Helper functions (PDF processing, API handling)
├── report_generator.py     # PDF Report generation logic
├── .env                    # Environment variables (API Keys)
├── requirements.txt        # Project dependencies
└── README.md               # Project Documentation
```

## Deployment
This app is ready to be deployed on Streamlit Community Cloud:

1. **Push to GitHub**: Ensure your project (including `requirements.txt`) is on a public GitHub repository.
2. **Login to Streamlit**: Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. **Create App**: Click **"New App"** and select your repository.
4. **Configure Secrets**:
   - Before deploying, click on **Advanced Settings** → **Secrets**.
   - Add your API Key in TOML format:
     ```toml
     GOOGLE_API_KEY = "your_google_api_key_here"
     ```
5. **Deploy**: Click the **Deploy** button. Your app will be live in minutes.

---

## Screenshots
*(Add screenshots of your Dashboard, Chat Assistant, and Risk Analysis here)*

---

## Contributing
Contributions are welcome! Please follow these steps:
1. **Fork** the repository.
2. Create a new **Branch** (`git checkout -b feature/NewFeature`).
3. **Commit** your changes.
4. **Push** to the branch.
5. Open a **Pull Request**.

---

## License
This project is licensed under the MIT License.

---

<div align="center">
  <b>Developed with ❤️ by <a href="https://github.com/PathakSiddhant">Siddhant Pathak</a></b>
</div>