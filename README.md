## ▶️ How to Run the Project
 
Follow the steps below in the given order.
---
1)Download ZIP

2)Open CMD in Project Root
   You should see:
          app.py
          backend/
          data/
          requirements.txt
          README.md

3)Install all required Python packages (requirements.txt)
    pip install -r requirements.txt

4)Set Groq API Key (Environment Variable)
    The application uses Groq for LLM-based summarization.
    Set your Groq API key as an environment variable.
     setx GROQ_API_KEY "your_groq_api_key_here"
    
After running this command:
* Close the current CMD
* Open a new CMD window
Verify the key is set:
    echo %GROQ_API_KEY%

5)Start the Backend (FastAPI)
In the project root, run:
python -m uvicorn backend.main:app --reload
Keep this terminal running.

6)Start the Frontend (Streamlit)
Open a second CMD window, again in the project root, and run:
python -m streamlit run app.py

7)Use the Application
Enter a valid patient_id (e.g. 1002)
Click Generate Summary
View structured clinical sections with citations
Invalid patient IDs (e.g. 9999) return a clear error message



FOLDER ARCHITECTURE

clinical-summary-generator/
│
├── app.py
│   └── Streamlit frontend (UI layer)
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation & run instructions
│
├── backend/
│   │
│   ├── main.py
│   │   └── FastAPI application (API layer)
│   │
│   ├── data_loader.py
│   │   └── CSV ingestion & patient-level data assembly
│   │
│   ├── summarizers/
│   │   ├── diagnoses.py
│   │   ├── vitals.py
│   │   ├── oasis.py
│   │   ├── wounds.py
│   │   ├── medications.py
│   │   └── __init__.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   ├── prompt.py
│   │   ├── composer.py
│   │   ├── utils.py
│   │   └── __init__.py
│   │
│   └── __init__.py
│
└── data/
    ├── diagnoses.csv
    ├── medications.csv
    ├── vitals.csv
    ├── wounds.csv
    ├── oasis.csv
    └── notes.csv   (intentionally not used)


