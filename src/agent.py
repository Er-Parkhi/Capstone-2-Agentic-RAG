from src.rag_pipeline import MedicalRAG


class MedicalAgent:
    def __init__(self):
        self.rag = MedicalRAG()

    def ask(self, question: str) -> str:
        return self.rag.answer(question)


if __name__ == "__main__":
    agent = MedicalAgent()
    print(agent.ask("What are the symptoms of diabetes?"))
