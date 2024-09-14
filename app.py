from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import pdfplumber
import mammoth
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.secret_key = 'fb7ce1a2f6dbc201d9290140813afea8'  # Set a secret key for session management

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.extract_raw_text(docx_file)
        return result.value

# Initialize HuggingFace Q&A model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_question(document_text, question):
    # Use HuggingFace's question-answering pipeline directly
    answer = qa_pipeline(question=question, context=document_text)
    return answer['answer']

# Route for file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text based on file type
        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            extracted_text = extract_text_from_docx(file_path)
        else:
            return jsonify({"error": "Unsupported file format"})

        # Store extracted text for future use in Q&A
        session['document_text'] = extracted_text  # This is critical
        print("Extracted Text:", extracted_text)  # Add this to debug
        return jsonify({"message": "File uploaded and text extracted successfully", "extracted_text": extracted_text[:500]})  # Limit text for testing
    return jsonify({"error": "File type not allowed"})


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    document_text = session.get('document_text', '')

    if not document_text:
        return jsonify({"error": "No document uploaded or text extracted"})

    # Answer the question based on the document
    answer = answer_question(document_text, question)
    return jsonify({"question": question, "answer": answer})


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
