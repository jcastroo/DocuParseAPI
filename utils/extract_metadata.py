import fitz  
import io

def extract_metadata(file_bytes: bytes) -> dict:
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        metadata = doc.metadata
        return {
            "title": metadata.get("title"),
            "author": metadata.get("author"),
            "pages": len(doc),
            "created_at": metadata.get("creationDate")
        }
