from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from config import CHUNK_SIZE,CHUNK_OVERLAP

EXTENSION_LANGUAGE_MAP={
    ".py":   Language.PYTHON,
    ".js":   Language.JS,
    ".ts":   Language.TS,
    ".jsx":  Language.JS, 
    ".tsx":  Language.TS, 
    ".java": Language.JAVA,
    ".cpp":  Language.CPP,
    ".c":    Language.C,
    ".go":   Language.GO,
    ".rs":   Language.RUST,
    ".html": Language.HTML,
    ".md":   Language.MARKDOWN,
}

def get_splitter(extension:str):
    language=EXTENSION_LANGUAGE_MAP.get(extension)
    if language:
        return RecursiveCharacterTextSplitter.from_language(
            language=language,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
    else:
        return RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
    
def chunk_file(files:list):
    all_chunks=[]
    for file in files:
        splitter=get_splitter(file['extension'])
        chunks=splitter.split_text(file['content'])
        for chunk in chunks:
            doc=Document(
                page_content=chunk,
                metadata={
                    "file_path":file['file_path'],
                    "extension":file['extension']
                }
            )
            all_chunks.append(doc)
    print(f"created {len(all_chunks)} chunks")
    return all_chunks
