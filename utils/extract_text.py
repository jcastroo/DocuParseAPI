from pdfminer.high_level import extract_text
import io

def extract_pdf_text(file_bytes: bytes) -> str:
    with io.BytesIO(file_bytes) as f:
        text = extract_text(f)
    return text.strip()
