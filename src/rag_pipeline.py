import os
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import AzureChatOpenAI

from src.ingest import build_vectorstore

load_dotenv()


class MedicalRAG:
    def __init__(self):
        self.vectorstore = build_vectorstore()

    def _get_relevant_context(self, question: str, top_k: int = 5) -> List[Document]:
        return self.vectorstore.similarity_search(question, k=top_k)

    def _fallback_answer(self, question: str, contexts: List[Document]) -> str:
        if not contexts:
            return "I couldn't find relevant information in the medical dataset for that question. Please ask about a symptom, disease, or treatment topic present in the dataset."

        best = contexts[0].page_content
        combined = "\n\n".join(doc.page_content for doc in contexts[:3])

        return (
            f"Based on the available medical dataset, the most relevant information is:\n\n{combined}\n\n"
            f"For your question: '{question}'\nA concise answer is: {best.split('Answer: ', 1)[-1] if 'Answer:' in best else best}"
        )

    def answer(self, question: str) -> str:
        if not question or not question.strip():
            return "Please enter a valid medical question."

        pipeline_docs = self._get_relevant_context(question)

        api_key = os.getenv("azure_api_key") or os.getenv("azure_embeddings_api_key")
        endpoint = os.getenv("azure_endpoint") or os.getenv("azure_embeddings_endpoint")
        deployment = os.getenv("azure_deployment") or os.getenv("azure_embeddings_deployment")

        if api_key and endpoint and deployment:
            try:
                llm = AzureChatOpenAI(
                    azure_endpoint=endpoint,
                    api_key=api_key,
                    azure_deployment=deployment,
                    api_version="2024-02-01",
                    temperature=0.2,
                )
                context = "\n\n".join(doc.page_content for doc in pipeline_docs[:4])
                prompt = (
                    "You are a helpful medical assistant. Use only the context below to answer the user's question. "
                    "If the answer is not clearly present, say you do not have enough evidence and suggest talking to a doctor.\n\n"
                    f"Context:\n{context}\n\nQuestion: {question}"
                )
                return llm.invoke(prompt).content
            except Exception:
                pass

        return self._fallback_answer(question, pipeline_docs)


def answer_question(question: str) -> str:
    return MedicalRAG().answer(question)


if __name__ == "__main__":
    sample_question = "What are the symptoms of diabetes?"
    print(answer_question(sample_question))

