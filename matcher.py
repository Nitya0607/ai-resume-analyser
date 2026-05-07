from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_entities

def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0, [], []
        
    jd_entities = extract_entities(job_description)
    resume_entities = extract_entities(resume_text)
    
    jd_skills = set([s.lower() for s in jd_entities['skills']])
    resume_skills = set([s.lower() for s in resume_entities['skills']])
    
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_description])
    semantic_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    semantic_score = semantic_similarity * 100
    
    if not jd_skills:
        score = round(semantic_score, 2)
        return score, [], ["No specific technical skills identified. Score based purely on semantic text matching."]
        
    matched_skills = jd_skills.intersection(resume_skills)
    exact_score = (len(matched_skills) / len(jd_skills)) * 100
    
    final_score = round((exact_score * 0.70) + (semantic_score * 0.30), 2)
    
    missing_skills = list(jd_skills - resume_skills)
    
    suggestions = []
    if missing_skills:
        for idx, skill in enumerate(missing_skills):
            if idx % 3 == 0:
                suggestions.append(f"Incorporate '{skill.title()}' naturally into your recent work experience bullets to show practical application.")
            elif idx % 3 == 1:
                suggestions.append(f"The job description specifically targets '{skill.title()}'. Consider adding a project or certification highlighting your expertise here.")
            else:
                suggestions.append(f"Ensure '{skill.title()}' is explicitly listed in your core Technical Skills section so the ATS easily parses it.")
    else:
        suggestions.append("Outstanding! Your skills align perfectly with all identified requirements in the job description.")
        
    if final_score < 50:
        suggestions.append("Your exact keyword match is quite low. Try tailoring your terminology to directly mirror the phrases used in the job description.")
    elif final_score > 80:
        suggestions.append("High match detected. Focus on describing the business impact of these skills rather than just listing them.")
        
    return final_score, missing_skills, suggestions
