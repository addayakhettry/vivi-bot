import pdfplumber
from docx import Document

def extract_text(file):
    filename = file.filename.lower()

    # TXT
    if filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    # PDF
    elif filename.endswith(".pdf"):
        file.stream.seek(0)
        with pdfplumber.open(file.stream) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages)

    # DOCX
    elif filename.endswith(".docx"):
        file.stream.seek(0)
        doc = Document(file.stream)
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

    return "[Unsupported file type]"
