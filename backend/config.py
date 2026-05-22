import os 
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL="llama-3.1-8b-instant"
EMBEDDING_MODEL='all-MiniLM-L6-v2'

CHUNK_SIZE=1000
CHUNK_OVERLAP=200

DATA_DIR = os.getenv("DATA_DIR", ".")
CHROMA_DB_PATH=os.path.join(DATA_DIR, "chroma_db")
REPOS_PATH=os.path.join(DATA_DIR, "repos")

IGNORED_DIRS={
    "node_modules",
    ".git",
    "venv",
    ".env",
    "__pycache__",
    ".DS_Store",
    "build",
    "dist",
    ".vscode",
    ".idea"
}


IGNORED_EXTENSIONS={
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".pdf", ".zip", ".tar", ".mp4", ".mp3",
    ".lock", ".bin", ".exe", ".wasm"
}

ALLOWED_EXTENSIONS={
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".cpp", ".c", ".go", ".rs",
    ".html", ".css", ".md", ".json", ".yaml", ".yml", ".sh", ".sql"
}

