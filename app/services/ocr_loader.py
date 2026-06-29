import os
import tempfile
import traceback

import easyocr
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Init once at module level (heavy model load)
reader = easyocr.Reader(["en"], gpu=False)  # set gpu=True if you have CUDA


def load_words_from_imagebasedpdf(uploaded_file: UploadFile):
    """Extract text from image-based/scanned PDF using EasyOCR and split into chunks"""
    print(f"[OCR] Loading: {uploaded_file.filename}")

    if not uploaded_file:
        raise ValueError("No PDF file provided")

    if not uploaded_file.filename.endswith(".pdf"):
        raise ValueError("File must be a PDF")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            uploaded_file.file.seek(0)  # Reset cursor since PyPDF already read it
            content = uploaded_file.file.read()
            print(f"[OCR] Read {len(content)} bytes")
            tmp.write(content)
            tmp_path = tmp.name
            print(f"[OCR] Temp file: {tmp_path}")

        print("[OCR] Converting PDF pages to images...")
        images = convert_from_path(tmp_path, dpi=200)
        print(f"[OCR] ✅ Converted {len(images)} pages")

        docs = []
        for i, image in enumerate(images):
            print(f"[OCR] Running OCR on page {i + 1}...")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as img_tmp:
                image.save(img_tmp.name, "JPEG")
                img_path = img_tmp.name

            try:
                result = reader.readtext(
                    img_path, detail=0
                )  # detail=0 returns just strings
                page_text = " ".join(result).strip()

                print(
                    f"[OCR] Page {i + 1}: {len(page_text)} chars — {page_text[:100] if page_text else '[EMPTY]'}"
                )

                if page_text:
                    docs.append(
                        Document(
                            page_content=page_text,
                            metadata={"source": uploaded_file.filename, "page": i},
                        )
                    )
            finally:
                os.unlink(img_path)

        if not docs:
            print("[OCR] ❌ No text extracted from any page")
            raise ValueError("OCR extracted no content from PDF")

        print(f"[OCR] ✅ Extracted text from {len(docs)} pages")

    except Exception as e:
        print(f"[OCR] ❌ Error: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise ValueError(f"OCR failed: {e}")
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
                print("[OCR] Cleaned up temp file")
            except:
                pass

    split_docs = text_splitter.split_documents(docs)
    print(f"[OCR] ✅ Split into {len(split_docs)} chunks")
    return split_docs
