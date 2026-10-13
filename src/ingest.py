import os
from pathlib import Path
from typing import List

import pandas as pd
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
INDEX_DIR = ROOT_DIR / "faiss_index"


def _get_embeddings():
    azure_embedding_key = os.getenv("azure_embeddings_api_key") or os.getenv("azure_api_key")
    azure_embedding_endpoint = os.getenv("azure_embeddings_endpoint") or os.getenv("azure_endpoint")
    azure_embedding_deployment = os.getenv("azure_embeddings_deployment") or os.getenv("azure_deployment")

    if azure_embedding_key and azure_embedding_endpoint and azure_embedding_deployment:
        return AzureOpenAIEmbeddings(
            azure_endpoint=azure_embedding_endpoint,
            api_key=azure_embedding_key,
            azure_deployment=azure_embedding_deployment,
            api_version="2024-02-01",
        )

    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def _get_dataset_path() -> Path:
    for filename in ["medical_dataset.csv", "healthcare_disease_dataset.csv", "Symptom2Disease.csv"]:
        candidate = DATA_DIR / filename
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"No supported dataset was found in {DATA_DIR}")


def _load_documents() -> List[Document]:
    dataset_path = _get_dataset_path()
    df = pd.read_csv(dataset_path)
    docs: List[Document] = []

    if {"question", "answer"}.issubset(df.columns):
        for _, row in df.iterrows():
            question = str(row.get("question", "")).strip()
            answer = str(row.get("answer", "")).strip()
            if not question and not answer:
                continue
            content = f"Question: {question}\nAnswer: {answer}" if question and answer else (question or answer)
            docs.append(Document(page_content=content, metadata={"source": dataset_path.name, "question": question}))
        return docs

    if {"label", "text"}.issubset(df.columns):
        for _, row in df.iterrows():
            label = str(row.get("label", "")).strip()
            text = str(row.get("text", "")).strip()
            if not label and not text:
                continue
            content = f"Disease: {label}\nDetails: {text}" if label and text else (label or text)
            docs.append(Document(page_content=content, metadata={"source": dataset_path.name, "disease": label}))
        return docs

    for _, row in df.iterrows():
        text = " ".join(str(value).strip() for value in row.tolist() if str(value).strip())
        if text:
            docs.append(Document(page_content=text, metadata={"source": dataset_path.name}))

    return docs


def build_vectorstore(force_rebuild: bool = False):
    index_dir = INDEX_DIR / "medical_index"
    index_dir.mkdir(parents=True, exist_ok=True)

    if not force_rebuild:
        faiss_path = index_dir / "index.faiss"
        pickle_path = index_dir / "index.pkl"
        if faiss_path.exists() and pickle_path.exists():
            try:
                return FAISS.load_local(folder_path=str(index_dir), embeddings=_get_embeddings(), allow_dangerous_deserialization=True)
            except Exception:
                pass

    documents = _load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, _get_embeddings())
    vectorstore.save_local(str(index_dir))
    return vectorstore


if __name__ == "__main__":
    build_vectorstore(force_rebuild=True)
    print(f"Built index at {INDEX_DIR / 'medical_index'}")
