import os
import tempfile
import streamlit as st
import plotly.graph_objects as go
from resume_parser import extract_text, extract_entities
from matcher import calculate_match_score

st.set_page_config(page_title="AI Resume Analyzer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput>div>div>input {
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
    }
    .css-1d391kg {
        background-color: #1e2530;
    }
    .metric-card {
        background-color: #1e2530;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .suggestion-item {
        padding: 10px;
        background-color: #2b3544;
        border-left: 4px solid #00ffcc;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    .missing-keyword {
        display: inline-block;
        background-color: #ff4b4b;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        margin: 4px;
        font-size: 0.85em;
    }
    .found-keyword {
        display: inline-block;
        background-color: #00cc66;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        margin: 4px;
        font-size: 0.85em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Resume Analyzer & Optimizer")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx"])

with col2:
    st.markdown("### Job Description")
    job_description = st.text_area("Paste the job description here", height=150)

if uploaded_file is not None and job_description:
    with st.spinner("Analyzing resume against job description..."):
        file_ext = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        resume_text = extract_text(tmp_file_path)
        os.unlink(tmp_file_path)
        
        if not resume_text.strip():
            st.error("Could not extract text from the uploaded file.")
        else:
            resume_entities = extract_entities(resume_text)
            
            score, missing_skills, suggestions = calculate_match_score(resume_text, job_description)
            
            st.markdown("---")
            
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.markdown("### Match Score")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Compatibility"},
                    gauge={
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#00ffcc"},
                        'bgcolor': "#1e2530",
                        'borderwidth': 2,
                        'bordercolor': "#333",
                        'steps': [
                            {'range': [0, 50], 'color': '#ff4b4b'},
                            {'range': [50, 75], 'color': '#ffa500'},
                            {'range': [75, 100], 'color': '#00cc66'}
                        ],
                    }
                ))
                fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                st.plotly_chart(fig, use_container_width=True)
            
            with res_col2:
                st.markdown("### Extracted Skills")
                if resume_entities['skills']:
                    skills_html = "".join([f'<span class="found-keyword">{skill}</span>' for skill in resume_entities['skills']])
                    st.markdown(f"<div>{skills_html}</div><br>", unsafe_allow_html=True)
                else:
                    st.write("No specific skills identified.")
                    
                st.markdown("### Missing Keywords")
                if missing_skills:
                    missing_html = "".join([f'<span class="missing-keyword">{skill.title()}</span>' for skill in missing_skills])
                    st.markdown(f"<div>{missing_html}</div><br>", unsafe_allow_html=True)
                else:
                    st.write("No missing key skills identified based on our common skill database.")
            
            st.markdown("### Actionable Suggestions")
            for suggestion in suggestions:
                st.markdown(f'<div class="suggestion-item">{suggestion}</div>', unsafe_allow_html=True)
                
            with st.expander("View Extracted Education & Experience"):
                col_ed, col_ex = st.columns(2)
                with col_ed:
                    st.markdown("**Education Institutions:**")
                    if resume_entities['education']:
                        for ed in resume_entities['education']:
                            st.write(f"- {ed}")
                    else:
                        st.write("No education details clearly identified.")
                with col_ex:
                    st.markdown("**Organizations/Experience:**")
                    if resume_entities['experience']:
                        for ex in resume_entities['experience']:
                            st.write(f"- {ex}")
                    else:
                        st.write("No specific organizational experience identified.")
