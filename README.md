# Smart Resume Analyzer

A Python-based web application that analyzes how well a resume matches a job description using machine learning techniques.

## Features
- Upload resume (PDF)
- Compare with job description
- Match score using TF-IDF & cosine similarity
- Matched and missing skills
- Suggestions for improvement

## Tech Stack
- Python
- Streamlit
- pandas
- PyPDF2
- scikit-learn

## Screenshots

![UI](assets/ui_1.png)
![Result](assets/ui_2.png)

## Run Project

```bash
pip install -r requirements.txt
streamlit run app.py