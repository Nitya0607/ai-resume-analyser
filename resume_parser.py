import os
import re
import spacy
import docx2txt
from PyPDF2 import PdfReader

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    os.system('python -m spacy download en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        pass
    return text

def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text if text else ""
    except Exception:
        return ""

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    return ""

def extract_entities(text):
    doc = nlp(text)
    entities = {
        'skills': [],
        'education': [],
        'experience': []
    }
    
    skill_keywords = [
        "python", "java", "javascript", "c++", "c#", "ruby", "php", "html", "css", "sql", 
        "nosql", "react", "angular", "vue", "node.js", "django", "flask", "spring", "aws", 
        "azure", "gcp", "docker", "kubernetes", "git", "machine learning", "deep learning", 
        "nlp", "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "agile", "scrum", "leadership", "communication", "project management", "rest api", "graphql"
    ]
    
    text_lower = text.lower()
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            entities['skills'].append(skill.title())
            
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'DATE']:
            if "university" in ent.text.lower() or "college" in ent.text.lower() or "institute" in ent.text.lower():
                if ent.text not in entities['education']:
                    entities['education'].append(ent.text)
            elif ent.label_ == 'ORG':
                if ent.text not in entities['experience']:
                    entities['experience'].append(ent.text)
                    
    return entities
