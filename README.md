# Financial AI Agent

Financial AI Agent allows users to upload financial data (CSV or Excel), ask questions about it in natural language, and get smart insights powered by LLMs like LLaMA-3 via LangChain.


## Features

- Upload CSV/XLS/XLSX financial data
- Preview uploaded data
- Ask questions in natural language
- Get structured, intelligent responses using LLMs
- FastAPI backend, Streamlit frontend

## Project Structure
```bash
Directory structure:
└── vivek02sharma-financial-ai-agent/
    ├── app.py
    ├── Dockerfile
    ├── main.py
    ├── requirements.txt
    ├── .dockerignore
    ├── agent/
    │   └── financial_agent.py
    ├── schema/
    │   └── schemas.py
    ├── Test-Files/
    │   ├── financial data.csv
    │   └── random data.xlsx
    └── utils/
        └── read_file.py
```

## Environment Variables
Make sure to set your GROQ API Key in a `.env` file:

```bash
GROQ_API_KEY=your_api_key_here
```

## Run with Docker

### 1. Build the backend image (FastAPI):

```bash
docker build -t financial-ai-backend .
```

### 2. Run the backend:

```bash
docker run -p 8000:8000 financial-ai-backend
```
### 3. Run the Streamlit:

```bash
streamlit run app.py
```

## API Endpoints

- GET / – Health check

- POST /upload – Upload a CSV or Excel file

- POST /query – Ask a question (requires file upload first)


## Sample Data
Use the CSV file in `Test-Files/financial data.csv` to try out the app with real-looking financial transactions.