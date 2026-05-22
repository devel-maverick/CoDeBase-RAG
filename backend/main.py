from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingest import ingest_repo
from chunker import chunk_file
from embedder import get_vector_db
from retriever import answer_query

app=FastAPI(title="CODE RAG API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    repo_url:str

class ChatRequest(BaseModel):
    question:str
    collection_name:str


@app.post('/ingest')
def ingest(request:IngestRequest):
    try:
        files=ingest_repo(request.repo_url)
        chunks=chunk_file(files)
        repo_name=request.repo_url.rstrip("/").split("/")[-1].replace(".git","")
        vectorstore=get_vector_db(chunks,repo_name)
        return {
            "message": "Repo ingested successfully!",
            "collection_name": repo_name,
            "files_processed": len(files),
            "chunks_created": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.post('/chat')
def chat(request:ChatRequest):
    try:
        result=answer_query(request.question,request.collection_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))