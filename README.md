# Automated CV Scoring and Feedback AI Agent

## Overview
This project aims to automate the process of scoring resumes and providing personalized feedback to candidates. It parses PDF/DOCX resumes, matches keywords with a job description (JD), and generates a score based on the content and experience. The feedback is then sent to candidates via email, helping recruiters streamline their hiring process.

## Features
- **Automated Resume Scoring**: Scores resumes based on their content and how well they align with a given job description.
- **Personalized Feedback**: Sends personalized feedback to each candidate based on their resume score.
- **Supports Multiple Formats**: Parses both PDF and DOCX resume formats.
- **Email Integration**: Sends automated feedback emails to candidates using SMTP.
- **Streamlit Deployment**: Deployed as an easy-to-use web app via Streamlit for real-time interaction.

## Technologies Used
- **Python**: Primary programming language for processing and automation.
- **Streamlit**: Web framework for building the interactive frontend.
- **PyPDF2** & **python-docx**: For parsing PDF and DOCX resume files.
- **Natural Language Processing (NLP)**: For keyword matching and resume scoring.
- **SMTP**: For email integration and sending feedback.

## Installation

### Prerequisites
- Python 3.6+
- Streamlit
- Required libraries (`PyPDF2`, `python-docx`, `smtplib`, `nltk`, etc.)

### Steps to Install
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/automated-cv-scoring-feedback.git
    ```

2. Navigate to the project folder:
    ```bash
    cd automated-cv-scoring-feedback
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application locally:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Upload a resume (in PDF or DOCX format).
2. Provide the job description (JD) text to match with.
3. Click on "Score Resume" to get a score based on the content and experience.
4. The system will generate a score and send personalized feedback to the candidate via email.

## Project Structure

```plaintext
automated-cv-scoring-feedback/
│
├── app.py              # Streamlit app for frontend
├── resume_parser.py    # Resume parsing and scoring logic
├── email_sender.py     # Email integration for feedback
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
