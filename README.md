# AI Resume Analyzer

I built this AI Resume Analyzer to help job seekers understand how well their resumes match up against specific job descriptions. It essentially acts like a local ATS (Applicant Tracking System), reading your resume, picking out your skills, and telling you exactly what keywords you're missing.

## What it does

*   **Reads your documents:** You can upload PDF or DOCX files, and it uses `spaCy` to read through them and pull out your education, experience, and specific technical skills.
*   **Scores your resume:** It uses Scikit-Learn (TF-IDF and Cosine Similarity) to compare the text in your resume against the text in a job description. This spits out a match score from 0 to 100%.
*   **Tells you what to fix:** It figures out which keywords from the job description are missing from your resume and suggests exactly what you should add to improve your score.
*   **Simple dashboard:** I built the frontend using Streamlit, so everything runs locally in a clean, dark-mode interface with a nice visual gauge for your score.

## Built with

*   **Frontend:** Streamlit, Plotly, custom HTML/CSS
*   **NLP & ML:** spaCy, Scikit-Learn
*   **Parsing:** PyPDF2, docx2txt
*   **Language:** Python 3.10+

## How to run it locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the required language model:**
   This app needs the `en_core_web_sm` model from spaCy to read the text properly.
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Start the app:**
   ```bash
   streamlit run app.py
   ```

Once it's running, just open the local URL (usually `http://localhost:8501`) in your browser, upload a resume, paste a job description, and see how well they match.

## License
This project is open-source under the MIT License.
