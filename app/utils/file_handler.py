import PyPDF2
from docx import Document

def extract_text_from_pdf(file_obj) -> str:
    text = ""
    reader = PyPDF2.PdfReader(file_obj)
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_obj) -> str:
    doc = Document(file_obj)
    return "\n".join(p.text for p in doc.paragraphs)
