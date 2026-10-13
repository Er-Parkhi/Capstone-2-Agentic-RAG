from pathlib import Path

import pandas as pd
import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.agent import MedicalAgent


ROOT = Path(__file__).resolve().parents[1]


class FakeVectorStore:
    def __init__(self, documents):
        self.documents = documents

    def similarity_search(self, question, k=5):
        return self.documents[:k]


class FakeEmbeddings(Embeddings):
    def _embedding(self, text):
        return [float(len(text)), float(text.lower().count("diabetes"))]

    def embed_documents(self, texts):
        return [self._embedding(text) for text in texts]

    def embed_query(self, text):
        return self._embedding(text)


def test_project_files_exist():
    assert (ROOT / "app.py").exists()
    assert (ROOT / "main.py").exists()
    assert (ROOT / "src" / "agent.py").exists()
    assert (ROOT / "src" / "rag_pipeline.py").exists()
    assert (ROOT / "src" / "ingest.py").exists()
    assert (ROOT / ".streamlit" / "config.toml").exists()
    assert (ROOT / ".github" / "workflows" / "ci.yml").exists()

    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    theme_config = (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")
    assert 'page_title="Doctor Chatty"' in app_source
    assert "<h1>Doctor Chatty</h1>" in app_source
    assert "--primary: #bd5d7b" in app_source
    assert 'primaryColor = "#bd5d7b"' in theme_config


@pytest.fixture
def agent_without_external_services(monkeypatch):
    monkeypatch.setattr(
        "src.rag_pipeline.build_vectorstore",
        lambda: FakeVectorStore(
            [
                Document(
                    page_content=(
                        "Question: Diabetes symptoms\n"
                        "Answer: Common symptoms include increased thirst and fatigue."
                    ),
                    metadata={},
                )
            ]
        ),
    )
    for variable in (
        "azure_api_key",
        "azure_embeddings_api_key",
        "azure_endpoint",
        "azure_embeddings_endpoint",
        "azure_deployment",
        "azure_embeddings_deployment",
    ):
        monkeypatch.delenv(variable, raising=False)
    return MedicalAgent()


def test_agent_handles_blank_question(agent_without_external_services):
    response = agent_without_external_services.ask("   ")

    assert "valid medical question" in response.lower()


def test_agent_returns_relevant_response_for_known_question(agent_without_external_services):
    response = agent_without_external_services.ask("What are the symptoms of diabetes?")

    assert "symptoms" in response.lower()
    assert "diabetes" in response.lower()


def test_dataset_loader_builds_documents(monkeypatch, tmp_path):
    from src import ingest

    dataset_path = tmp_path / "medical_dataset.csv"
    pd.DataFrame(
        [{"question": "What are diabetes symptoms?", "answer": "Increased thirst and fatigue."}]
    ).to_csv(dataset_path, index=False)
    monkeypatch.setattr(ingest, "DATA_DIR", tmp_path)

    documents = ingest._load_documents()

    assert len(documents) == 1
    assert "diabetes symptoms" in documents[0].page_content
    assert documents[0].metadata["source"] == dataset_path.name


def test_vectorstore_builds_from_dataset(monkeypatch, tmp_path):
    from src import ingest

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    pd.DataFrame(
        [{"question": "What are diabetes symptoms?", "answer": "Increased thirst and fatigue."}]
    ).to_csv(data_dir / "medical_dataset.csv", index=False)
    monkeypatch.setattr(ingest, "DATA_DIR", data_dir)
    monkeypatch.setattr(ingest, "INDEX_DIR", tmp_path / "indexes")
    monkeypatch.setattr(ingest, "_get_embeddings", FakeEmbeddings)

    vectorstore = ingest.build_vectorstore(force_rebuild=True)
    results = vectorstore.similarity_search("diabetes symptoms", k=1)

    assert len(results) == 1
    assert "diabetes symptoms" in results[0].page_content
