import os
import shutil
from git import Repo
from config import REPOS_PATH,IGNORED_DIRS,IGNORED_EXTENSIONS,ALLOWED_EXTENSIONS


def clone_repo(repo_url:str):

    repo_name=repo_url.rstrip("/").split("/")[-1].replace(".git","")

    local_path=os.path.join(REPOS_PATH,repo_name)

    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    os.makedirs(REPOS_PATH,exist_ok=True)
    print(f"cloning {repo_url}...")
    Repo.clone_from(repo_url,local_path)
    print(f"clone to: {local_path}")

    return local_path

def load_files(repo_path:str):
    files=[]
    for root,dirs,filenames in os.walk(repo_path):
        dirs[:]=[d for d in dirs if d not in IGNORED_DIRS]
        for filename in filenames:
            ext=os.path.splitext(filename)[1].lower()
            if ext in IGNORED_EXTENSIONS:
                continue
            if ext not in ALLOWED_EXTENSIONS:
                continue
            file_path=os.path.join(root,filename)
            relative_path=os.path.relpath(file_path,repo_path)
            try:
                with open(file_path,"r",encoding="utf-8",errors="ignore") as f:
                    content=f.read()
                if not content.strip():
                    continue
                files.append({
                    "file_path":relative_path,
                    "content":content,
                    "extension":ext
                })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
    print(f"loaded {len(files)} files")
    return files

def ingest_repo(repo_url:str):
    repo_path=clone_repo(repo_url)
    files=load_files(repo_path)
    return files