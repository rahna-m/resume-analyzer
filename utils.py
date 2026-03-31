# contains backend processing logic
import re
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "html", "css", "sql",
    "mysql", "mongodb", "react", "nodejs", "streamlit", "django", "flask",
    "machine learning", "data analysis", "pandas", "numpy", "oop",
    "communication", "teamwork", "problem solving", "git", "github",
    "excel", "power bi", "aws", "api", "bootstrap"
]

def extract_text_from_pdf(uploaded_file):   #reads the uploaded PDF then extracts text from all pages
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    except Exception:
        return ""
    return text

def preprocess_text(text):    #clean raw text before comparison
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# calculate similarity percentage between resume and job description
# def calculate_match_score(resume_text, job_description):
#     documents = [resume_text, job_description]
#     # vectorizer = CountVectorizer().fit_transform(documents)
#     vectorizer = TfidfVectorizer().fit_transform(documents)
#     similarity = cosine_similarity(vectorizer)[0][1]
#     return round(similarity * 100)
def calculate_match_score(resume_text, job_description, resume_skills, jd_skills):
    # 1. Text similarity (TF-IDF)
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    similarity = cosine_similarity(vectorizer)[0][1]
    similarity_score = similarity * 100

    # 2. Skill match %
    if len(jd_skills) > 0:
        matched = set(resume_skills).intersection(set(jd_skills))
        skill_match_percentage = (len(matched) / len(jd_skills)) * 100
    else:
        skill_match_percentage = 0

    # 3. Final score (combined)
    final_score = (similarity_score * 0.6) + (skill_match_percentage * 0.4)

    return round(final_score)

# def extract_skills(text):
#     text = text.lower()
#     found_skills = []

#     for skill in SKILL_KEYWORDS:
#         if skill in text:
#             found_skills.append(skill)

#     return found_skills

def extract_skills(text): #identify important skills from the text
    text = text.lower()

    # Split text into clean words
    words = set(text.replace("/", " ").replace(",", " ").split())

    found_skills = []

    for skill in SKILL_KEYWORDS:
        skill_lower = skill.lower()

        # Special handling for 'c'
        if skill_lower == "c":
            # match ONLY if exact word 'c' exists
            if "c" in words or "c language" in text or "c programming" in text:
                found_skills.append(skill)

        else:
            # split multi-word skills like "rest api"
            skill_words = skill_lower.split()

            if len(skill_words) == 1:
                if skill_lower in words:
                    found_skills.append(skill)
            else:
                # for multi-word skills
                if skill_lower in text:
                    found_skills.append(skill)

    return found_skills