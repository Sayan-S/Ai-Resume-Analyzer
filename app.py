import streamlit as st
from pypdf import PdfReader
import config
from providers import ask_openai, ask_gemini

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="ATS AI Studio | Resume Analyzer",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------- DARK THEME CSS -----------------
st.markdown(
    """
    <style>
    /* Global background and text */
    .stApp {
        background-color: #0d0f12;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #f0f6fc !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Header Gradient Banner */
    .main-header {
        text-align: center;
        padding: 2.2rem 1rem 1.5rem 1rem;
        border-radius: 16px;
        background: linear-gradient(180deg, #161b22 0%, #0d0f12 100%);
        border: 1px solid #30363d;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-bottom: 0.8rem;
    }

    /* Card Containers */
    .card-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    }

    /* File uploader container */
    [data-testid="stFileUploader"] {
        background: #111418;
        border: 1px dashed #388bfd;
        border-radius: 10px;
        padding: 1rem;
    }

    /* Text areas */
    .stTextArea textarea {
        background-color: #111418 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-size: 0.95rem;
    }
    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.25) !important;
    }

    /* Primary Action Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 16px rgba(46, 160, 67, 0.35) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 160, 67, 0.5) !important;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- HEADER -----------------
st.markdown(
    """
    <div class="main-header">
        <span class="badge">Next-Gen ATS Engine</span>
        <h1>⚡ AI Resume Screener & Job Matcher</h1>
        <p style="color: #8b949e; font-size: 1rem; margin-top: 0.4rem;">
            Upload your candidate resume, input the target job description, and get instant talent diagnostics.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- STEP 1: RESUME UPLOAD (STACKED) -----------------
st.markdown("### 1. Candidate Resume")
uploaded_file = st.file_uploader("Upload candidate resume in PDF format", type=["pdf"])

resume_text = ""
page_count = 0
word_count = 0

if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        page_count = len(reader.pages)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                resume_text += extracted + "\n"
        word_count = len(resume_text.split())

        # Metric summary for recruiter
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Status", "Parsed ✓")
        m_col2.metric("Pages", f"{page_count}")
        m_col3.metric("Word Count", f"{word_count}")

    except Exception as e:
        st.error(f"Error parsing PDF file: {e}")

st.write("")

# ----------------- STEP 2: JOB DESCRIPTION (STACKED) -----------------
st.markdown("### 2. Job Description & Requirements")
job_desc = st.text_area(
    "Target Job Description (JD)",
    height=200,
    placeholder="Paste key responsibilities, qualifications, required tools, and must-have skillsets here...",
)

st.write("")

# ----------------- STEP 3: ANALYSIS MODE (FEATURE ADDITION) -----------------
st.markdown("### 3. Evaluation Mode")
eval_mode = st.radio(
    "Select screening depth:",
    [
        "Comprehensive ATS Diagnostic (Score, Gaps & Keywords)",
        "Executive Summary (Fast Recruit Go/No-Go Decision)",
        "Interview Prep Generator (Tailored Questions & Edge Cases)",
    ],
    horizontal=True,
)

st.write("")

# ----------------- EXECUTION & DISPLAY -----------------
if st.button("Run AI Diagnostics ⚡", type="primary"):
    if not resume_text:
        st.warning("⚠️ Please upload a valid PDF resume first.")
    elif not job_desc.strip():
        st.warning("⚠️ Please provide a target job description.")
    else:
        with st.spinner("Analyzing candidate profile against requirements..."):
            # Select prompt based on evaluation mode
            if "Comprehensive" in eval_mode:
                prompt = f"""
You are an executive Technical Recruiter and ATS evaluation algorithm.
Evaluate the candidate's resume strictly against the target Job Description.

### CANDIDATE RESUME:
{resume_text}

### JOB DESCRIPTION:
{job_desc}

Provide a structured, highly scannable analysis:
1. **Match Score**: State a numerical score (0-100%) and a concise 2-sentence rationale.
2. **Core Competency Alignment**: Key strengths and exact skills that match the requirements.
3. **Critical Skill & Keyword Gaps**: Must-have technologies or credentials present in the JD but absent from the resume.
4. **ATS Parsing & Impact Recommendations**: Actionable bullet points on how the candidate can quantify bullet points and optimize keywords.
5. **Hiring Recommendation**: (Strong Fit / Potential Fit / Not Recommended) with reason.
"""
            elif "Executive" in eval_mode:
                prompt = f"""
You are a Senior Talent Acquisition Lead conducting a 30-second rapid screening review.
Resume:
{resume_text}

Job Description:
{job_desc}

Output:
1. **Candidate Synopsis**: 3 bullet summary of qualifications.
2. **Estimated Fit Percentage**: (0-100%).
3. **Primary Pros & Cons**: Top 2 advantages and top 2 dealbreakers.
4. **Final Recommendation**: Hire / Interview / Reject.
"""
            else:
                prompt = f"""
You are a hiring manager preparing an interview for this candidate based on their gaps.
Resume:
{resume_text}

Job Description:
{job_desc}

Output:
1. **Candidate Verification Questions**: 3 questions assessing areas where their resume claims match JD requirements.
2. **Gap Assessment Questions**: 3 challenging technical or behavioral questions probing areas missing or vague in the resume.
3. **Suggested Role Fit Level**: Junior / Mid / Senior.
"""

            try:
                if config.PROVIDER == "openai":
                    analysis = ask_openai(prompt)
                elif config.PROVIDER == "gemini":
                    analysis = ask_gemini(prompt)
                else:
                    analysis = "Ollama is running locally and cannot be queried via cloud hosting."

                st.markdown("---")
                st.markdown("### 📊 Screening Report")
                st.markdown(analysis)

                # Export option
                st.download_button(
                    label="📥 Download Screening Report (.txt)",
                    data=analysis,
                    file_name="candidate_ats_evaluation.txt",
                    mime="text/plain",
                )

            except Exception as err:
                st.error(f"Analysis failed: {err}")