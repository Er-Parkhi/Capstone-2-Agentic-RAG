from src.agent import MedicalAgent


def main():
    agent = MedicalAgent()
    while True:
        question = input("\nAsk a medical question (or type 'quit' to exit): ").strip()
        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break
        print("\nAnswer:")
        print(agent.ask(question))


if __name__ == "__main__":
    main()
