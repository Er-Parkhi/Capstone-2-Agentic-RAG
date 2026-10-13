# Doctor Chatty

Doctor Chatty is a local medical question-answering app built with Python, LangChain, and FAISS. It loads a healthcare dataset, embeds the content, retrieves the most relevant documents, and answers user questions in a Streamlit interface.

## Features
- FAISS-based vector retrieval
- Local medical dataset search
- Streamlit web interface
- Fallback answers when external Azure/OpenAI credentials are unavailable

## Project structure
- `app.py` — Streamlit UI entry point
- `main.py` — terminal-based chat interface
- `src/agent.py` — agent wrapper
- `src/rag_pipeline.py` — retrieval + answer logic
- `src/ingest.py` — dataset ingestion and FAISS index creation
- `data/` — sample medical datasets

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:

   python -m pip install -r requirements.txt

4. Run the app:

   python -m streamlit run app.py

5. Open the local URL shown by Streamlit in the browser.

## Notes
- The app is designed to run without Azure credentials by falling back to the local medical dataset and a local embedding model.
- If you want to use Azure OpenAI, add your environment variables in a `.env` file.
- Do not commit secrets to GitHub.

## Tests and CI

Run the tests locally with:

```powershell
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

The GitHub Actions workflow in `.github/workflows/ci.yml` runs all tests on pushes, pull requests, and manual workflow dispatches. Tests use a mocked vector store and a temporary CSV dataset, so they do not need Azure credentials or download an embedding model.

## Example question
- What are the symptoms of diabetes?
- How can I improve my sleep quality?
- What are the treatment options for arthritis?
