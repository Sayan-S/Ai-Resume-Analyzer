import streamlit as st
from pypdf import PdfReader
import config
from providers import ask_openai, ask_gemini

st.set_page_config(page_title="AI Resume Analyzer & ATS Scorer", page_icon="📄", layout="centered")

st.title("📄 AI Resume Analyzer & Job Matcher")
st.markdown("Upload a candidate resume and paste the job description to get an automated ATS match score and analysis.")

# 1. Resume Upload (Top)
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
resume_text = ""
if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text
        st.success("Resume uploaded and parsed successfully!")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# 2. Job Description (Bottom)
job_desc = st.text_area("Paste Job Description (JD)", height=220, placeholder="Paste the target job description or core skills here...")

# 3. Analyze Action
if st.button("Analyze Resume", type="primary"):
    if not resume_text:
        st.warning("Please upload a valid PDF resume first.")
    elif not job_desc.strip():
        st.warning("Please provide a job description to evaluate against.")
    else:
        with st.spinner("Analyzing match score and evaluating qualifications..."):
            prompt = f"""
You are an expert HR Talent Acquisition Specialist and ATS evaluation system.
Evaluate the candidate's resume against the provided Job Description (JD).

### Candidate Resume:
{resume_text}

### Target Job Description:
{job_desc}

Provide your analysis in the following structured format:
1. **Overall Match Percentage**: (e.g., 85/100) with a 2-sentence rationale.
2. **Key Strengths & Relevant Experience**: Bullet points highlighting matching qualifications.
3. **Missing Skills / Keyword Gaps**: Specific tools, skills, or requirements in the JD not found in the resume.
4. **Actionable Recommendations**: Clear, specific suggestions to tailor the resume for this position.
"""
            try:
                if config.PROVIDER == "openai":
                    analysis = ask_openai(prompt)
                elif config.PROVIDER == "gemini":
                    analysis = ask_gemini(prompt)
                else:
                    analysis = "Ollama is running locally and cannot be reached from the cloud."

                st.subheader("Analysis Results")
                st.markdown(analysis)
            except Exception as err:
                st.error(f"Analysis failed: {err}")