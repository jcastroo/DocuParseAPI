from fastapi import FastAPI, Request, File, UploadFile
from auth import APIKeyMiddleware
from utils.extract_text import extract_pdf_text
from utils.extract_metadata import extract_metadata
from utils.extract_entities import extract_entities

app = FastAPI(title="DocuParse API")

app.add_middleware(APIKeyMiddleware)

@app.post("/extract")
async def extract(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    text = extract_pdf_text(contents)
    metadata = extract_metadata(contents)
    entities = extract_entities(text)

 

    return {
        "text": text,
        "metadata": metadata,
        "entities": entities
    }
