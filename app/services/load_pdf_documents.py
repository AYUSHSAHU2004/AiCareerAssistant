from fastapi import UploadFile
import tempfile
import os
import traceback
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Define before function

def load_pdf_documents(uploaded_file: UploadFile):
    """Load PDF and split into chunks"""
    print(f"[PDF] Loading: {uploaded_file.filename}")
    
    if not uploaded_file:
        print(f"[PDF] ❌ No file provided")
        raise ValueError("No PDF file provided")
    
    if not uploaded_file.filename.endswith('.pdf'):
        print(f"[PDF] ❌ Not a PDF file: {uploaded_file.filename}")
        raise ValueError("File must be a PDF")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = uploaded_file.file.read()
            print(f"[PDF] Read {len(content)} bytes")
            tmp.write(content)
            tmp_path = tmp.name
            print(f"[PDF] Temp file: {tmp_path}")

        print(f"[PDF] Loading with PyPDFLoader...")
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        print(f"[PDF] ✅ Loaded {len(docs)} pages")
        
        # DEBUG: Print each page
        for i, doc in enumerate(docs):
            content_preview = doc.page_content[:100] if doc.page_content else "[EMPTY]"
            print(f"[PDF] Page {i}: {len(doc.page_content)} chars - {content_preview}")
        
        if not docs:
            print(f"[PDF] ❌ No pages extracted from PDF")
            raise ValueError("No content extracted from PDF")
            
    except Exception as e:
        print(f"[PDF] ❌ Error loading PDF: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise ValueError(f"Failed to load PDF: {e}")
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
                print(f"[PDF] Cleaned up temp file")
            except:
                pass

    split_docs = text_splitter.split_documents(docs)
    print(f"[PDF] ✅ Split into {len(split_docs)} chunks")
    return split_docs
