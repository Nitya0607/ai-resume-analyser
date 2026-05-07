import os
import random
import spacy
from spacy.training.example import Example

def get_training_data():
    return [
        ("I have 5 years of experience using Python for data analysis.", {"entities": [(31, 37, "SKILL"), (42, 55, "SKILL")]}),
        ("Built web applications using React and Node.js.", {"entities": [(29, 34, "SKILL"), (39, 46, "SKILL")]}),
        ("Skilled in developing Machine Learning models with TensorFlow.", {"entities": [(22, 38, "SKILL"), (51, 61, "SKILL")]}),
        ("Implemented CI/CD pipelines utilizing Jenkins and Docker.", {"entities": [(12, 17, "SKILL"), (38, 45, "SKILL"), (50, 56, "SKILL")]}),
        ("Designed scalable cloud architectures on AWS.", {"entities": [(41, 44, "SKILL")]}),
        ("Proficient in writing complex SQL queries.", {"entities": [(30, 33, "SKILL")]}),
        ("Managed agile teams using Scrum methodologies.", {"entities": [(8, 13, "SKILL"), (26, 31, "SKILL")]}),
        ("Developed microservices using Spring Boot and Java.", {"entities": [(10, 23, "SKILL"), (30, 41, "SKILL"), (46, 50, "SKILL")]}),
        ("Experience with state management in Redux.", {"entities": [(36, 41, "SKILL")]}),
        ("Strong understanding of Object-Oriented Programming.", {"entities": [(24, 51, "SKILL")]}),
        ("Deployed applications on Kubernetes clusters.", {"entities": [(25, 35, "SKILL")]}),
        ("Familiar with NoSQL databases like MongoDB.", {"entities": [(14, 19, "SKILL"), (35, 42, "SKILL")]}),
        ("Created REST APIs using Flask.", {"entities": [(8, 17, "SKILL"), (24, 29, "SKILL")]}),
        ("Automated infrastructure provisioning with Terraform.", {"entities": [(43, 52, "SKILL")]}),
        ("Good communication and leadership skills.", {"entities": [(5, 18, "SKILL"), (23, 33, "SKILL")]}),
        ("Proficient in Git version control.", {"entities": [(14, 17, "SKILL")]})
    ]

def train_custom_ner_model(output_dir="custom_skill_ner", iterations=30):
    train_data = get_training_data()
    
    nlp = spacy.blank("en")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")
        
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
            
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            random.shuffle(train_data)
            losses = {}
            for text, annotations in train_data:
                example = Example.from_dict(nlp.make_doc(text), annotations)
                nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
                
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    nlp.to_disk(output_dir)

if __name__ == "__main__":
    train_custom_ner_model()
