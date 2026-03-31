# This is the main frontend and control file
import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, preprocess_text, calculate_match_score, extract_skills

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="📄", layout="wide")

def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("""
<div class="main-header">
    <h1>📄 Smart Resume Analyzer</h1>
    <p>Analyze your resume and compare it with a job description</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF only)", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Paste Job Description")
    job_description = st.text_area("Enter the job description here", height=250)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("Analyze Resume"):
    if uploaded_file is not None and job_description.strip() != "":
        resume_text = extract_text_from_pdf(uploaded_file)

        if resume_text.strip() == "":
            st.error("Could not read text from the uploaded PDF.")
        else:
            processed_resume = preprocess_text(resume_text)
            processed_jd = preprocess_text(job_description)

            score = calculate_match_score(processed_resume, processed_jd)

            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(job_description)

            matched_skills = sorted(list(set(resume_skills).intersection(set(jd_skills))))
            missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))

            st.markdown("---")
            st.subheader("Analysis Result")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>Match Score</h3>
                    <h2>{score}%</h2>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>Matched Skills</h3>
                    <h2>{len(matched_skills)}</h2>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="metric-box">
                    <h3>Missing Skills</h3>
                    <h2>{len(missing_skills)}</h2>
                </div>
                """, unsafe_allow_html=True)

            st.progress(score / 100)

            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Matched Skills")
                st.write(", ".join(matched_skills) if matched_skills else "No matched skills found.")
                st.markdown('</div>', unsafe_allow_html=True)

            with res_col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Missing Skills")
                st.write(", ".join(missing_skills) if missing_skills else "No missing skills found.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Suggestions")
            if score >= 80:
                st.success("Your resume is strongly aligned with the job description.")
            elif score >= 60:
                st.warning("Your resume is moderately matched. Add more relevant keywords and skills.")
            else:
                st.error("Your resume needs improvement. Include more job-related skills and project experience.")

            if missing_skills:
                st.info("Try adding these skills if you have experience with them: " + ", ".join(missing_skills))
            st.markdown('</div>', unsafe_allow_html=True)

            data = {
                "Category": ["Match Score", "Matched Skills Count", "Missing Skills Count"],
                "Value": [f"{score}%", len(matched_skills), len(missing_skills)]
            }
            df = pd.DataFrame(data)
            st.subheader("Summary Table")
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Please upload a resume and enter a job description.")