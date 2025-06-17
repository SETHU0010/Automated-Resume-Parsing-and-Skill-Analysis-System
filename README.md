# 🧠 Intelligent Resume Parser using AI and Regex

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-yellow.svg)
![PDF](https://img.shields.io/badge/Support-.pdf%20%2F%20.docx-brightgreen)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-ff69b4)

---

## ❓ Problem Statement

Recruiters and hiring managers face challenges when screening large volumes of resumes. Manually extracting relevant information such as **skills, experience, and qualifications** is:

- Time-consuming  
- Error-prone  
- Inconsistent  

This slows down the hiring process and increases the risk of overlooking qualified candidates.

---

## 🎯 Aim

To automate the extraction of structured information from resumes by building a web application that uses both **traditional regex-based methods** and **modern AI (Google Gemini)** for **intelligent parsing**.

---

## 🥅 Goal

- ✅ Minimize manual resume screening.
- ✅ Improve accuracy and consistency in data extraction.
- ✅ Support scalable and quick parsing of `.pdf` and `.docx` files.
- ✅ Provide a simple, user-friendly interface to view extracted metadata.

---

## 💡 Solution Overview

The system extracts structured metadata like:

- 🧑 Name, 📞 Phone Number, 📧 Email
- 🛠️ Skills, 💼 Experience, 🎓 Education
- 📜 Certifications

### 🔍 Dual Extraction Strategy:

1. **Primary Method (AI-based)**: Google Gemini API – context-aware, high-accuracy extraction.
2. **Fallback Method (Regex-based)**: Traditional regex & keyword match when AI fails.

---

## ✅ Advantages

- ⚙️ **Automated Parsing**: Eliminates manual extraction.
- 🚀 **Fast and Scalable**: Processes multiple resumes quickly.
- 🧠 **AI-Enhanced Extraction**: Improves accuracy and handles contextual data.
- 🔄 **Fallback Logic**: Regex ensures extraction even when AI fails.
- 📄 **Format Agnostic**: Supports `.pdf` and `.docx` formats.
- 🌐 **Web Interface**: Easy-to-use Flask-based front-end.

---

## ⚠️ Disadvantages

- 🌐 **Dependency on Gemini API**: Needs internet access and API key.
- 💰 **Cost Factor**: Google Gemini API usage may incur charges.
- 📉 **Regex Limitations**: May not handle edge cases or complex resume formats.
- 🔒 **Privacy Concerns**: Resume data must be handled securely.
- 🧾 **Format Issues**: Poorly formatted PDFs may lead to extraction errors.

---

## 🚀 Features

- 📤 Upload resumes in `.pdf` and `.docx` formats
- 🧾 Extracts clean text from resume files
- 🧠 Context-aware parsing via Google Gemini API
- 🪝 Regex-based fallback extraction
- 🧩 Returns structured JSON metadata
- 🌐 Simple and intuitive web interface using Flask
- 🔒 Handles file uploads securely with validation

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|--------------------------------------|
| Backend      | Python, Flask                        |
| AI Service   | Google Gemini API                    |
| Text Parsing | PyPDF2, python-docx                  |
| Extraction   | Regex, Keyword Matching              |
| Frontend     | HTML, CSS (Bootstrap)                |
| Data Format  | JSON Output                          |

---

## 🧱 Architecture
+----------------+ +---------------------+
| Upload Resume | --> | Text Extraction |
+----------------+ | (.pdf/.docx Parsing) |
+----------+----------+
|
v
+-----------------------------------+
| Metadata Extraction (AI + Regex) |
+--------+--------------------------+
|
v
+-------------------------------+
| Return Structured JSON Output |
+-------------------------------+


---

## 🧪 Sample Output (JSON)

```json
{
  "name": "Sethumadhavan V",
  "email": "sethumadhavanvelu2002@gmail.com",
  "phone": "9159299878",
  "skills": ["Python", "Flask", "SQL", "Power BI", "Machine Learning"],
  "education": [
    {
      "degree": "M.Tech in Software Engineering",
      "university": "Vellore Institute of Technology",
      "cgpa": "7.65"
    }
  ],
  "experience": [
    {
      "role": "Data Science Intern",
      "company": "XYZ Company",
      "duration": "Jan 2024 - Apr 2024"
    }
  ],
  "certifications": [
    "Power BI Essentials",
    "SQL for Data Analysis"
  ]
}

📂 Project Structure

intelligent-resume-parser/
│
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html         # Upload form UI
│   └── result_ai.html     # Results page UI
├── static/                # CSS/JS files (optional)
├── resume_parser/
│   ├── extractor.py       # Regex and keyword-based methods
│   ├── gemini_api.py      # Gemini API integration
│   └── utils.py           # Helper functions
├── uploads/               # Uploaded resumes (auto-created)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation


🧑‍💻 How to Run Locally
Clone the Repository

bash
Copy
Edit
git clone https://github.com/SETHU0010/intelligent-resume-parser.git
cd intelligent-resume-parser
Create a Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Add Your Gemini API Key

Create a .env file and include:

env
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key_here
Run the Application

bash
Copy
Edit
python app.py
Visit in Browser

cpp
Copy
Edit
http://127.0.0.1:5000/
📈 Future Enhancements
🧠 Add support for ChatGPT / Claude API fallback

📊 Add visual dashboard for parsed data summary

🖇️ Connect to ATS systems or HR databases

🔐 Implement user authentication for multi-user environments

📂 Add bulk upload and zip file support

☁️ Deploy using Docker or Streamlit Cloud

👨‍💻 Author
Sethumadhavan V
📧 sethumadhavanvelu2002@gmail.com
📱 +91 91592 99878
🌐 GitHub: SETHU0010

