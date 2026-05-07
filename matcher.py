import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_entities

def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0, [], []
        
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_description])
    
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)
    
    jd_entities = extract_entities(job_description)
    resume_entities = extract_entities(resume_text)
    
    jd_skills = set([s.lower() for s in jd_entities['skills']])
    resume_skills = set([s.lower() for s in resume_entities['skills']])
    
    missing_skills = list(jd_skills - resume_skills)
    
    suggestions = []
    if missing_skills:
        for skill in missing_skills:
            suggestions.append(f"Add '{skill.title()}' to your skills section to improve your match by optimizing for ATS keywords.")
    else:
        suggestions.append("Your skills align perfectly with the identified keywords in the job description.")
        
    if score < 50:
        suggestions.append("Consider using more vocabulary directly from the job description to improve overall semantic similarity.")
        
    return score, missing_skills, suggestions
