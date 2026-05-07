# AI Resume Analyzer 🚀

An intelligent, NLP-powered Resume Analyzer that evaluates uploaded resumes against job descriptions, extracting key information and providing actionable optimization feedback in real-time.

## Features ✨

*   **Intelligent Data Extraction:** Uses `spaCy` to process PDF and DOCX files, accurately extracting entities like Skills, Education, and Experience.
*   **NLP Matching Engine:** Leverages Scikit-Learn's `TfidfVectorizer` and Cosine Similarity to calculate a precise 0-100% Match Score between a resume and a job description.
*   **Keyword Optimization:** Cross-references extracted skills to automatically identify missing keywords and generate actionable improvement suggestions.
*   **Modern Interactive UI:** Built on Streamlit with custom CSS and Plotly, featuring a sleek dark mode, a dynamic circular gauge chart for the match score, and structured feedback panels.

## Tech Stack 🛠️

*   **Frontend & Dashboard:** Streamlit, Plotly, HTML/CSS
*   **NLP & Machine Learning:** spaCy, Scikit-Learn
*   **Document Parsing:** PyPDF2, docx2txt
*   **Core Logic:** Python 3.10+

## Installation & Setup 💻

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the spaCy language model:**
   This project relies on the `en_core_web_sm` model to process text for Named Entity Recognition.
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage 🎯

Run the Streamlit application from your terminal:
```bash
streamlit run app.py
```

1. Open the provided Local URL (typically `http://localhost:8501`) in your web browser.
2. Drag and drop a sample resume (`.pdf` or `.docx`).
3. Paste the target Job Description in the text area.
4. The dashboard will automatically analyze the documents, calculate the match score, and provide real-time suggestions on how to improve the resume for ATS systems.

## License 📄
This project is open-source and available under the MIT License.
