▶️ How to Run the Project

Follow the steps exactly in the order below.

1️⃣ Download the Project
* Download the project as a ZIP file
* Extract it to a local directory

2️⃣ Open Command Prompt in Project Root
* Navigate to the extracted project folder and open CMD there.
* You should see the following files and folders:

      app.py
      backend/
      data/
      requirements.txt
      README.md

3️⃣ Install Required Python Packages
* Install all dependencies listed in requirements.txt:

      pip install -r requirements.txt

4️⃣ Set Groq API Key (Environment Variable)
* This application uses Groq for LLM-based clinical summarization.
* Set your Groq API key as an environment variable:

      setx GROQ_API_KEY "your_groq_api_key_here"
* After running this command:
* Close the current CMD window
* Open a new CMD window
* Verify the environment variable is set correctly:

      echo %GROQ_API_KEY%
* You should see your API key printed.

5️⃣ Start the Backend (FastAPI)
* In the project root directory, run:

      python -m uvicorn backend.main:app --reload


* This starts the FastAPI backend
* Keep this terminal running

6️⃣ Start the Frontend (Streamlit)
* Open a second CMD window in the project root and run:

      python -m streamlit run app.py
* This launches the Streamlit UI.

7️⃣ Use the Application
* Enter a valid patient_id (example: 1002)
* Click Generate Summary
* View structured clinical sections with citations
❌ Invalid patient IDs (example: 9999) will return a clear error message

📁 Folder Architecture\
clinical-summary-generator/
├── app.py                  # Streamlit UI (Frontend)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── backend/                # Core Logic (API Layer)
│   ├── main.py             # FastAPI entry point
│   ├── data_loader.py      # CSV ingestion & data assembly
│   ├── summarizers/        # Domain-specific logic
│   │   ├── diagnoses.py
│   │   ├── vitals.py
│   │   ├── oasis.py
│   │   ├── wounds.py
│   │   └── medications.py
│   └── llm/                # AI Generation Layer
│       ├── client.py       # API connection (OpenAI/Anthropic/Local)
│       ├── prompt.py       # System & User prompt templates
│       ├── composer.py     # Logic to stitch sections together
│       └── utils.py        # Token counting & LLM helpers
└── data/                   # Raw CSV Patient Data
    ├── diagnoses.csv
    ├── medications.csv
    ├── vitals.csv
    ├── wounds.csv
    └── oasis.csv
