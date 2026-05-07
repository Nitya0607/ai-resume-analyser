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
        "agile", "scrum", "leadership", "communication", "project management", "rest api", "graphql",
        "typescript", "swift", "kotlin", "go", "rust", "r", "matlab", "scala", "perl", "bash",
        "linux", "unix", "windows", "macos", "android", "ios", "react native", "flutter", "dart",
        "express.js", "next.js", "nuxt.js", "svelte", "jquery", "bootstrap", "tailwind css", "sass",
        "less", "webpack", "babel", "vite", "graphql", "apollo", "mongodb", "postgresql", "mysql",
        "sqlite", "oracle", "sql server", "redis", "memcached", "cassandra", "elasticsearch", "firebase",
        "supabase", "rabbitmq", "kafka", "celery", "nginx", "apache", "jenkins", "gitlab ci", "github actions",
        "travis ci", "circleci", "terraform", "ansible", "chef", "puppet", "promethues", "grafana",
        "elk stack", "splunk", "datadog", "new relic", "jira", "confluence", "trello", "asana",
        "figma", "sketch", "adobe xd", "photoshop", "illustrator", "invision", "zeplin", "wireframing",
        "prototyping", "user research", "usability testing", "a/b testing", "google analytics", "seo",
        "sem", "content marketing", "email marketing", "social media marketing", "copywriting",
        "salesforce", "hubspot", "tableau", "power bi", "looker", "excel", "word", "powerpoint",
        "problem solving", "critical thinking", "teamwork", "collaboration", "time management",
        "adaptability", "creativity", "emotional intelligence", "conflict resolution", "decision making",
        "public speaking", "presentation skills", "negotiation", "customer service", "data engineering",
        "computer vision", "natural language processing", "reinforcement learning", "big data", "hadoop",
        "spark", "hive", "pig", "zookeeper", "flume", "sqoop", "oozie", "mahout", "storm", "flink",
        "blockchain", "smart contracts", "solidity", "ethereum", "web3", "cybersecurity", "penetration testing",
        "ethical hacking", "cryptography", "network security", "cloud security", "devsecops", "ci/cd",
        "microservices", "serverless", "restful architecture", "soap", "grpc", "websockets", "oauth",
        "jwt", "saml", "openid", "sso", "active directory", "ldap", "tcp/ip", "dns", "http", "https",
        "ftp", "ssh", "ssl/tls", "vpn", "firewalls", "routers", "switches", "load balancing"
    ]
    
    text_lower = text.lower()
    text_normalized = re.sub(r'[\-\/\_]', ' ', text_lower)
    for skill in skill_keywords:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, text_lower) or re.search(pattern, text_normalized):
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
