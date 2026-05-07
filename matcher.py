from resume_parser import extract_entities

def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0, [], []
        
    jd_entities = extract_entities(job_description)
    resume_entities = extract_entities(resume_text)
    
    jd_skills = set([s.lower() for s in jd_entities['skills']])
    resume_skills = set([s.lower() for s in resume_entities['skills']])
    
    if not jd_skills:
        score = 100.0 if resume_skills else 0.0
        return score, [], ["No specific technical skills were identified in the job description."]
        
    matched_skills = jd_skills.intersection(resume_skills)
    score = round((len(matched_skills) / len(jd_skills)) * 100, 2)
    
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
        
    if score < 50:
        suggestions.append("Your exact keyword match is quite low. Try tailoring your terminology to directly mirror the phrases used in the job description.")
    elif score > 80:
        suggestions.append("High match detected. Focus on describing the business impact of these skills rather than just listing them.")
        
    return score, missing_skills, suggestions
