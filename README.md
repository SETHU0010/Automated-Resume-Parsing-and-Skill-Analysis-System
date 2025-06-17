# 🧠 Automated Resume Parsing and Skill Analysis System

A Flask-based AI-enhanced web application that intelligently parses resumes and extracts structured metadata (skills, education, contact info, experience) using both traditional and modern NLP methods, including Google Gemini API and regex fallback mechanisms.

---

## 📌 Problem Statement

Recruiters and hiring managers often face the challenge of sifting through large volumes of resumes to find suitable candidates. Manual resume screening is **time-consuming**, **error-prone**, and **inconsistent**, often leading to missed opportunities and inefficient hiring processes.

---

## 🎯 Aim

To develop an automated system that extracts relevant structured metadata from resumes in `.pdf` and `.docx` formats, thereby improving recruitment efficiency through AI-powered parsing.

---

## 🥅 Goal

- Automate the resume screening process.
- Extract information like name, email, phone, skills, education, and experience.
- Enhance accuracy using AI (Google Gemini) and ensure fallback support through regex.
- Build a user-friendly web interface for uploading and viewing results.

---

## ✅ Solution

- A web application developed using **Flask**.
- Supports **resume uploads** in `.pdf` and `.docx` formats.
- Extracts plain text using:
  - `PyPDF2` for PDFs
  - `python-docx` for DOCX files
- Uses two-stage metadata extraction:
  1. **Primary Method:** Google Gemini API (Generative AI)
  2. **Fallback Method:** Regex and keyword-based extraction
- Displays structured information in JSON format and via a results webpage.

---

## 🚀 Features

- 🔍 AI-powered resume metadata extraction
- 📄 Multi-format file support (.pdf and .docx)
- 🔁 Fallback parsing using regex
- 🧠 Real-time resume ranking and skill similarity
- 📤 Secure file upload with `secure_filename()`
- 🌐 Clean and interactive web UI
- 🧾 Outputs structured JSON metadata

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

## 🔧 Tech Stack

| Category        | Technologies Used                                  |
|-----------------|----------------------------------------------------|
| **Backend**     | Python, Flask, Regex, Gemini API                   |
| **Frontend**    | HTML, CSS                                          |
| **Parsing**     | PyPDF2, python-docx                                |
| **NLP**         | Sentence-BERT, Cosine Similarity                   |
| **AI Services** | Google Gemini API (Generative AI)                  |

---

## 🧭 Workflow

```text
User Uploads Resume (.pdf/.docx)
        ↓
Extract Text Using PyPDF2 / python-docx
        ↓
Chunk Large Texts (Optional)
        ↓
Primary Parsing: Google Gemini API
        ↓         ↘
 Success      Failure
   ↓             ↓
Structured Metadata (JSON) via Regex
        ↓
Display Results on Web Page (result_ai.html)

##  📌 Conclusion
This project bridges the gap between manual resume screening and modern AI-driven automation. By combining AI (Gemini) and traditional regex techniques, it delivers a flexible, scalable, and intelligent resume parser suitable for recruiters, HR platforms, and job portals.


Let me know if you'd like me to create a `requirements.txt`, Dockerfile, or `app.py` template for your project as well.
