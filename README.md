# Voice-Eval-Service


#Objective

This microservice analyzes short audio clips (≤ 60 seconds) and gives feedback on:

- Pronunciation accuracy
- Speaking pace (words per minute)
- Pause patterns
- Natural language feedback summary

# Setup Instructions

1. Clone the repo or copy the folder
2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# Setup & Run Instructions

 Install Dependencies

```bash
pip install -r requirements.txt
Run the FastAPI server:

bash
Copy
Edit
uvicorn main:app --reload
#
