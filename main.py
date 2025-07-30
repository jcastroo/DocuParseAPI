from fastapi import FastAPI, Request, File, UploadFile
from auth import APIKeyMiddleware
from utils.extract_text import extract_pdf_text
from utils.extract_metadata import extract_metadata
from utils.extract_entities import extract_entities

app = FastAPI(title="DocuParse API")

# Adiciona o middleware
app.add_middleware(APIKeyMiddleware)

# Endpoint principal
@app.post("/extract")
async def extract(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    text = extract_pdf_text(contents)
    metadata = extract_metadata(contents)
    entities = extract_entities(text)

    return {
        "text": text,
        "metadata": metadata,
        "entities": entities,
        "plan": request.state.plan  
    }
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/docs")
async def docs():
    return {
        "description": "DocuParse API - Extract text, metadata, and entities from PDF files.",
        "endpoints": {
            "/extract": "POST - Upload a PDF file to extract text, metadata, and entities.",
            "/health": "GET - Check the health status of the API."
        }
    }
# Endpoint de versão
@app.get("/version")
async def version():
    return {"version": "1.0.0", "description": "Initial release of DocuParse API."}
# Endpoint de exemplo
@app.get("/example")
async def example():
    return {
        "message": "This is an example endpoint.",
        "data": {
            "example_key": "example_value"
        }
    }