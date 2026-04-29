# Intelligent Chatbot for Banking

A fully functional, AI-powered banking chatbot built with Python, Flask, and scikit-learn. This project demonstrates Natural Language Processing (NLP) intent classification and simulates real banking operations through a web interface.

## Features

- **NLP Intent Recognition**: Uses TF-IDF and Logistic Regression to understand user queries.
- **Context-Aware Authentication**: Simulates a login flow asking for Account ID and PIN when sensitive information is requested.
- **Banking Operations Simulator**: Fetches mock balance and transaction data from a SQLite database.
- **Responsive UI**: A modern, clean chat interface built with HTML, CSS, and JavaScript.

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Setup Instructions

### Quick Start (Copy & Paste)
```bash
cd banking_chatbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Step-by-Step Instructions

1. **Navigate to the Project Directory**
   ```bash
   cd banking_chatbot
   ```

2. **Create a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   Start the Flask server:
   ```bash
   python app.py
   ```
   *Note: On the first run, the NLP model will automatically train itself using `intents.json` and the database will initialize with sample users.*

5. **Access the Chatbot**
   Open your web browser and go to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Sample Users for Testing

When the application runs for the first time, it creates the following sample accounts in the SQLite database:

| Name | Account ID | PIN |
|---|---|---|
| Alice Smith | 1001 | 1234 |
| Bob Johnson | 1002 | 5678 |

## How to Test

Try typing these queries into the chatbot:
- "Hi" or "Hello"
- "What is my balance?" (It will prompt you to login with Account ID `1001` and PIN `1234`)
- "Show my recent transactions"
- "I want to apply for a loan"
- "I lost my credit card"
