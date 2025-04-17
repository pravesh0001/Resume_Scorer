
import streamlit as st
import os
import re
import docx
import fitz  # PyMuPDF
import pandas as pd
import smtplib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from email.message import EmailMessage

# Extract resume text
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return ""

# JD Text
def get_jd_text():
    return """
    We are seeking candidates with strong experience in Artificial Intelligence and Data Science.
    Core expectations include knowledge of:

    - Python programming
    - Numpy, Pandas, and Matplotlib
    - OpenCV for computer vision
    - Power BI for data visualization
    - Machine Learning and Deep Learning concepts
    - Generative AI (GenAI) techniques
    - Excellent problem-solving and communication skills

    A degree in Computer Science or a related field is expected.
    Prior experience with model deployment and data wrangling is a plus.
    """

# Resume scoring
def score_resume(text):
    jd_text = get_jd_text()
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([text, jd_text])
    jd_score = round(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100, 2)

    education = bool(re.search(r"(b\.tech|bachelor|master|m\.tech|ph\.d)", text.lower()))
    ai_keywords = len(re.findall(r"(machine learning|deep learning|nlp|neural network|ai|cv|transformer|llm)", text.lower()))
    experience_years = len(re.findall(r"(\d+)\+?\s+(years|yrs)", text.lower()))

    score = min(jd_score + ai_keywords*3 + experience_years*5 + (10 if education else 0), 100)

    return {
        "JD Match Score": jd_score,
        "AI Keyword Count": ai_keywords,
        "Education Found": education,
        "Years of Experience (est)": experience_years,
        "Total CV Score": score
    }

# Email extraction and masking
def extract_email(text):
    matches = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return matches[0] if matches else "Not found"

def mask_email(email):
    if email != "Not found":
        name, domain = email.split('@')
        return f"{name[0]}****@{domain}"
    return email

def mask_name(text):
    match = re.search(r"(?i)(?:name\s*[:\-]?\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text)
    if match:
        parts = match.group(1).split()
        return f"{parts[0][0]}{'*' * (len(parts[0]) - 1)} {'*' * len(parts[1])}" if len(parts) > 1 else parts[0]
    return "Anonymous"

# Email sending
def send_feedback_email(receiver_email, name, score_details):
    msg = EmailMessage()
    msg['Subject'] = "Your Resume Feedback & Score"
    msg['From'] = "sharmapravesh175@gmail.com"
    msg['To'] = receiver_email

    feedback = f"""
Hi {name},

Thank you for submitting your resume. Here's a brief summary of your evaluation:

📊 Total CV Score: {score_details['Total CV Score']}
🔍 JD Match Score: {score_details['JD Match Score']}
📚 Education Found: {"Yes" if score_details['Education Found'] else "No"}
💡 AI Keyword Hits: {score_details['AI Keyword Count']}
🧠 Estimated Experience (Years): {score_details['Years of Experience (est)']}

✅ Strengths: {'Good match with JD' if score_details['JD Match Score'] > 60 else 'Some alignment'}
⚠️ Improvement Area: {'Add more AI keywords' if score_details['AI Keyword Count'] < 5 else 'Looks good'}

We encourage you to continue sharpening your profile. Feel free to apply again after making improvements.

All the best!
Team Elint
"""
    msg.set_content(feedback)

    # Email login and sending (make sure to allow less secure apps or use App Password)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("sharmapravesh175@gmail.com", "qyaa kqnl mjwh bges")
        smtp.send_message(msg)

# Streamlit UI
st.set_page_config(page_title="Resume Scorer", page_icon="📄")
st.title("📄 Automated Resume Scoring and Feedback")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully.")

    text = extract_text(uploaded_file.name)
    result = score_resume(text)
    name = mask_name(text)
    email = extract_email(text)

    st.subheader("📝 Evaluation Report")
    for k, v in result.items():
        st.write(f"**{k}**: {v}")

    st.write("**Masked Name:**", name)
    st.write("**Masked Email:**", mask_email(email))

    if email != "Not found":
        send_feedback_email(email, name, result)
        st.success("✅ Feedback email sent to candidate.")
    else:
        st.warning("⚠️ Email not found in resume.")
