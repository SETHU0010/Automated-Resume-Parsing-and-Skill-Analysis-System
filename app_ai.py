import os
import re
import json
import io
import pandas as pd
from flask import Flask, request, render_template, jsonify, session, send_file
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename
from docx import Document
import PyPDF2
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDvcBJWFC1feCLrdYL5SzccT1dbSTFRTRs")

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

UPLOAD_FOLDER = 'Music/Internship/project -2/sethu/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Load SentenceTransformer (currently unused but kept for future semantic tasks)
model = SentenceTransformer('all-MiniLM-L6-v2')

# File format check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Text extraction
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text(file_path):
    if file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format.")

# Define skills and keywords for extraction (same as your original code)
skills_dict = {
    "front_end_skills": [
        "HTML", "CSS", "JavaScript", "React", "Angular", "Vue", "TypeScript", "Responsive Web Design", 
        "CSS Preprocessors", "Sass", "LESS", "Web Performance Optimization", "Cross-browser Compatibility", 
        "UI/UX Design Principles", "Front-end Testing", "Jest", "Mocha", "Version Control", "Git"
    ],
    "back_end_skills": [
        "Python", "Java", "Ruby", "PHP", "C#", "Node.js", "RESTful API Design", "GraphQL", 
        "Server-Side Frameworks", "Express.js", "Django", "Flask", "Spring Boot", "Ruby on Rails", 
        "Authentication", "Authorization", "JWT", "OAuth", "Microservices Architecture", "Serverless Computing", 
        "Cloud Services", "AWS", "Azure", "Google Cloud", "Containerization", "Docker", "Kubernetes", 
        "Database Integration", "Back-end Testing", "JUnit", "Mocha", "Postman"
    ],
    "database_skills": [
        "Relational Databases", "MySQL", "PostgreSQL", "SQL Server", "Oracle", "NoSQL Databases", 
        "MongoDB", "Cassandra", "CouchDB", "Firebase", "Database Design", "Normalization", "SQL Query Optimization", 
        "Stored Procedures", "Triggers", "Database Indexing", "Data Modeling", "Data Migration", "ETL", 
        "Backup and Recovery", "Distributed Databases"
    ],
    "ai_skills": [
        "Machine Learning", "Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Deep Learning", 
        "Neural Networks", "CNNs", "RNNs", "Natural Language Processing", "NLP", "Computer Vision", "TensorFlow", 
        "PyTorch", "Keras", "Data Preprocessing", "Feature Engineering", "Model Evaluation", "Hyperparameter Tuning", 
        "AI Ethics", "AI Deployment", "ONNX", "TensorFlow Serving", "Reinforcement Learning Algorithms"
    ],
    "data_science_skills": [
        "Data Analysis", "Pandas", "NumPy", "Data Visualization", "Matplotlib", "Seaborn", "Plotly", "Statistical Analysis", 
        "Hypothesis Testing", "Regression", "Machine Learning", "Scikit-learn", "XGBoost", "Data Wrangling", 
        "Time Series Analysis", "Big Data", "Hadoop", "Spark", "Data Pipelines", "Airflow", "Luigi", "SQL for Data Analysis", 
        "A/B Testing", "Experimental Design", "Cloud-based Data Science Tools", "Google Colab", "Jupyter Notebooks"
    ]
}

# Regex-based metadata extraction (same as your original code)
def extract_metadata(text):
    metadata = {
        "name": "",
        "email": "",
        "phone": "",
        "years_experience": 0,
        "front_end_skills": [],
        "back_end_skills": [],
        "database_skills": [],
        "ai_skills": [],
        "data_science_skills": [],
        "location": "",
        "projects": [],
        "graduation": "",
        "graduation_year": "",
        "post_graduation": "",
        "post_graduation_year": "",
        "certifications": [],
        "summary": "",
        "internships": []  # New field
    }

    name_pattern = re.compile(r'^[A-Za-z]+(?: [A-Za-z]+)+')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    phone_pattern = re.compile(r'\+?\d{1,2}[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    experience_pattern = re.compile(r'(\d+)\s+year[s]? experience', re.IGNORECASE)
    summary_pattern = re.compile(r'(summary|professional summary|about me):?\s*([\s\S]+?)(\n[A-Z]|$)', re.IGNORECASE)
    internship_pattern = re.compile(r'(internship|intern)\s+(at|with)?\s*([\w\s&.-]+)', re.IGNORECASE)

    if name_match := name_pattern.search(text):
        metadata["name"] = name_match.group(0)
    if email_match := email_pattern.search(text):
        metadata["email"] = email_match.group(0)
    if phone_match := phone_pattern.search(text):
        metadata["phone"] = phone_match.group(0)
    if experience_match := experience_pattern.search(text):
        metadata["years_experience"] = int(experience_match.group(1))
    if summary_match := summary_pattern.search(text):
        metadata["summary"] = summary_match.group(2).strip()
    if internship_matches := internship_pattern.findall(text):
        metadata["internships"] = list(set(match[2].strip() for match in internship_matches if match[2].strip()))

    for skill in skills_dict["front_end_skills"]:
        if skill.lower() in text.lower():
            metadata["front_end_skills"].append(skill)
    for skill in skills_dict["back_end_skills"]:
        if skill.lower() in text.lower():
            metadata["back_end_skills"].append(skill)
    for skill in skills_dict["database_skills"]:
        if skill.lower() in text.lower():
            metadata["database_skills"].append(skill)
    for skill in skills_dict["ai_skills"]:
        if skill.lower() in text.lower():
            metadata["ai_skills"].append(skill)
    for skill in skills_dict["data_science_skills"]:
        if skill.lower() in text.lower():
            metadata["data_science_skills"].append(skill)

    return metadata

# Gemini API metadata extraction
def extract_metadata_with_gemini(text):
    prompt = (
        "Extract the following fields from the resume and return the result as a valid JSON object:\n"
        "Name, Email, Phone, Years of Experience, Summary, Skills (Front-end, Back-end, Database, AI, Data Science),\n"
        "Location, Projects, Graduation and Post-Graduation (with year), Certifications, and Internships (with company name).\n\n"
        f"Resume Text:\n{text}"
    )

    model = genai.GenerativeModel("gemini-1.5-pro")
    try:
        response = model.generate_content(prompt,
            generation_config=genai.GenerationConfig(temperature=0.0)
        )
        parsed = json.loads(response.text)
        return parsed
    except Exception as e:
        print(f"Gemini parsing error: {e}")
        return extract_metadata(text)  # Fallback

# Routes
@app.route('/')
def index():
    return render_template('result_ai.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    if len(uploaded_files) == 0:
        return jsonify({'error': 'No files uploaded'}), 400

    metadata_list = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(file_path)

            try:
                resume_text = extract_text(file_path)
                if not resume_text:
                    return jsonify({'error': f"Failed to extract text from {filename}"}), 400

                try:
                    metadata = extract_metadata_with_gemini(resume_text)
                except Exception as e:
                    print(f"Fallback to regex: {str(e)}")
                    metadata = extract_metadata(resume_text)

                metadata_list.append({"filename": filename, "metadata": metadata})
            except Exception as e:
                return jsonify({'error': f"Error processing {filename}: {str(e)}"}), 400
        else:
            return jsonify({'error': 'Unsupported file format. Please upload .pdf or .docx files only.'}), 400

    session['metadata_list'] = metadata_list
    return jsonify(metadata_list)

@app.route('/download_excel')
def download_excel():
    metadata_list = session.get('metadata_list')
    if not metadata_list:
        return "No metadata available to download.", 400

    rows = []
    for entry in metadata_list:
        filename = entry.get('filename')
        md = entry.get('metadata', {})
        row = {
            'Filename': filename,
            'Name': md.get('name', ''),
            'Email': md.get('email', ''),
            'Phone': md.get('phone', ''),
            'Years of Experience': md.get('years_experience', ''),
            'Location': md.get('location', ''),
            'Summary': md.get('summary', ''),
            'Front-end Skills': ", ".join(md.get('front_end_skills', [])),
            'Back-end Skills': ", ".join(md.get('back_end_skills', [])),
            'Database Skills': ", ".join(md.get('database_skills', [])),
            'AI Skills': ", ".join(md.get('ai_skills', [])),
            'Data Science Skills': ", ".join(md.get('data_science_skills', [])),
            'Projects': ", ".join(md.get('projects', [])) if isinstance(md.get('projects'), list) else md.get('projects', ''),
            'Graduation': md.get('graduation', ''),
            'Graduation Year': md.get('graduation_year', ''),
            'Post Graduation': md.get('post_graduation', ''),
            'Post Graduation Year': md.get('post_graduation_year', ''),
            'Certifications': ", ".join(md.get('certifications', [])),
            'Internships': ", ".join(md.get('internships', []))
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resumes')
        writer.save()
    output.seek(0)

    return send_file(output, download_name="resume_metadata.xlsx", as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
