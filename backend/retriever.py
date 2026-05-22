from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import GROQ_API_KEY, LLM_MODEL
from embedder import load_vectorstore


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0.4
    )


def get_prompt():
    system_prompt = """You are a senior software engineer helping understand a codebase.
Use the following code context to answer the question.
Always mention which file the code is from.
If you don't know, say 'I could not find this in the codebase.'

Context:
{context}"""
    return ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', '{question}')
    ])


def format_docs(docs):
    return "\n\n".join([
        f"File: {doc.metadata.get('file_path', 'unknown')}\n{doc.page_content}"
        for doc in docs
    ])


def answer_query(question: str, collection_name: str) -> dict:
    vectorstore = load_vectorstore(collection_name)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)
    context = format_docs(docs)
    prompt = get_prompt()
    llm = get_llm()
    messages = prompt.format_messages(context=context, question=question)
    response = llm.invoke(messages)

    sources = list(set([
        doc.metadata.get("file_path", "unknown") for doc in docs
    ]))

    return {
        "answer": response.content,
        "sources": sources
    }