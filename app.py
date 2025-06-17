import os
import re
import torch
import numpy as np
import zipfile
import io
from flask import Flask, request, render_template, jsonify, send_from_directory, send_file
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload folder and configure allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load BERT model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)


def allowed_file(filename):
    """Check if the uploaded file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")
    return text.strip()


def extract_text(file_path):
    """Extract text from a DOCX or PDF file."""
    if file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .docx or .pdf file.")


def calculate_similarity(job_emb, resume_embs):
    """Calculate cosine similarity between job and resume embeddings."""
    cosine_scores = cosine_similarity(job_emb.cpu().numpy().reshape(1, -1),
                                      resume_embs.cpu().numpy())
    return cosine_scores.flatten()


def get_top_n_resumes(resume_files, similarity_scores, n=5):
    """Get the top N resumes based on similarity scores."""
    top_n_indices = similarity_scores.argsort()[-n:][::-1]
    top_resumes = [(resume_files[i], float(similarity_scores[i])) for i in top_n_indices]
    return top_resumes


# Regex patterns for name and email extraction
name_pattern = re.compile(r'^[A-Za-z]+(?: [A-Za-z]+)+')
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

def extract_metadata(text):
    """Extract name and email from text."""
    metadata = {}
    # Extract Name
    name_match = name_pattern.search(text)
    if name_match:
        metadata["name"] = name_match.group(0)
    # Extract Email
    email_match = email_pattern.search(text)
    if email_match:
        metadata["email"] = email_match.group(0)
    return metadata


@app.route('/')
def index():
    """Render the upload page."""
    return render_template('uploads.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and similarity comparison."""
    job_description = request.form['job_description']
    uploaded_files = request.files.getlist('files')

    if not job_description:
        return jsonify({'error': 'Job description is required.'}), 400

    if not uploaded_files:
        return jsonify({'error': 'No files uploaded.'}), 400

    resume_texts = []
    resume_files = []
    metadata_list = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                resume_text = extract_text(file_path)
                if not resume_text:
                    return jsonify({'error': f"No text found in {filename}."}), 400
                resume_texts.append(resume_text)
                resume_files.append(filename)
                # Extract name and email metadata from the resume
                metadata = extract_metadata(resume_text)
                metadata_list.append(metadata)
            except Exception as e:
                return jsonify({'error': f"Error processing {filename}: {str(e)}"}), 400

    # Compute embeddings for job description and resumes
    texts = [job_description] + resume_texts
    embeddings = model.encode(texts, convert_to_tensor=True, device=device)
    job_embedding = embeddings[0]
    resume_embeddings = embeddings[1:]

    # Calculate similarity scores
    similarity_scores = calculate_similarity(job_embedding, resume_embeddings)

    # Get top matching resumes
    top_resumes = get_top_n_resumes(resume_files, similarity_scores, n=len(resume_files))

    # Combine the top resumes with metadata (name and email)
    result = []
    for resume, metadata in zip(top_resumes, metadata_list):
        resume_data = {
            'filename': resume[0],
            'similarity_score': resume[1],
            'metadata': metadata
        }
        result.append(resume_data)

    return jsonify(result)


@app.route('/top5', methods=['POST'])
def top_five_resumes():
    """Handle request for top 5 resumes."""
    job_description = request.form['job_description']
    uploaded_files = request.files.getlist('files')

    if not job_description:
        return jsonify({'error': 'Job description is required.'}), 400

    if not uploaded_files:
        return jsonify({'error': 'No files uploaded.'}), 400

    resume_texts = []
    resume_files = []
    metadata_list = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                resume_text = extract_text(file_path)
                if not resume_text:
                    return jsonify({'error': f"No text found in {filename}."}), 400
                resume_texts.append(resume_text)
                resume_files.append(filename)
                # Extract name and email metadata from the resume
                metadata = extract_metadata(resume_text)
                metadata_list.append(metadata)
            except Exception as e:
                return jsonify({'error': f"Error processing {filename}: {str(e)}"}), 400

    # Compute embeddings for job description and resumes
    texts = [job_description] + resume_texts
    embeddings = model.encode(texts, convert_to_tensor=True, device=device)
    job_embedding = embeddings[0]
    resume_embeddings = embeddings[1:]

    # Calculate similarity scores
    similarity_scores = calculate_similarity(job_embedding, resume_embeddings)

    # Get top 5 matching resumes
    top_resumes = get_top_n_resumes(resume_files, similarity_scores, n=5)

    # Combine the top resumes with metadata (name and email)
    result = []
    for resume, metadata in zip(top_resumes, metadata_list):
        resume_data = {
            'filename': resume[0],
            'similarity_score': resume[1],
            'metadata': metadata
        }
        result.append(resume_data)

    return jsonify(result)


@app.route('/download/emails', methods=['POST'])
def download_emails():
    """Generate and send the email list as a .txt file."""
    result_data = request.json  # Receive the results from the front-end
    if not result_data:
        return jsonify({'error': 'No results provided.'}), 400

    email_list = []
    for result in result_data:
        if result['metadata'] and 'email' in result['metadata']:
            email_list.append(result['metadata']['email'])

    # Create a .txt file with the email list
    email_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'emails.txt')
    with open(email_file_path, 'w') as email_file:
        for email in email_list:
            email_file.write(email + '\n')

    return send_from_directory(app.config['UPLOAD_FOLDER'], 'emails.txt', as_attachment=True)


@app.route('/download/top5', methods=['POST'])
def download_top5_zip():
    """Generate and send the top 5 resumes as a ZIP file."""
    result_data = request.json  # Receive the results from the front-end
    if not result_data:
        return jsonify({'error': 'No results provided.'}), 400

    # Get top 5 resumes from the results data
    top_5_resumes = result_data[:5]

    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for resume in top_5_resumes:
            resume_filename = resume['filename']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
            
            if os.path.exists(file_path):
                zip_file.write(file_path, arcname=resume_filename)

    zip_buffer.seek(0)  # Reset the buffer position to the start

    return send_file(zip_buffer, as_attachment=True, download_name='top_5_resumes.zip', mimetype='application/zip')


@app.route('/download/<filename>')
def download_file(filename):
    """Serve the resume file for download."""
    # Ensure the file exists in the uploads folder
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return jsonify({'error': 'File not found.'}), 404
        
@app.route('/download/remaining-emails', methods=['POST'])
def download_remaining_emails():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Extract emails from remaining resumes
    emails = [item['metadata']['email'] for item in data if 'metadata' in item and 'email' in item['metadata']]

    if not emails:
        return jsonify({"error": "No emails found"}), 404

    # Create a text file in memory
    email_text = "\n".join(emails)
    memory_file = io.BytesIO()
    memory_file.write(email_text.encode('utf-8'))
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, download_name="remaining_emails.txt", mimetype="text/plain")


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
