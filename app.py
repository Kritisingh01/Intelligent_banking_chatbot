from flask import Flask, request, jsonify, render_template, session
from model import IntentClassifier
import database
import os

app = Flask(__name__)
app.secret_key = "super_secret_key" # Required for session management

# Initialize database
if not os.path.exists(database.DB_NAME):
    database.init_db()

# Initialize and load model
nlp_model = IntentClassifier()
try:
    nlp_model.load_model()
except FileNotFoundError:
    print("Training model for the first time...")
    nlp_model.train()
    nlp_model.load_model()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
        
    # Check if user is in middle of login flow
    if session.get("awaiting_login"):
        return handle_login(user_message)
        
    # Get intent prediction
    prediction = nlp_model.get_response(user_message)
    tag = prediction["tag"]
    response = prediction["response"]
    
    # Handle specific intents requiring logic
    if tag == "balance":
        if not session.get("logged_in"):
            session["awaiting_login"] = True
            return jsonify({"response": "To check your balance, please log in first. What is your 4-digit Account ID?"})
        
        balance = database.get_balance(session.get("account_id"))
        response = f"Your current account balance is ${balance:.2f}."
        
    elif tag == "transactions":
        if not session.get("logged_in"):
            session["awaiting_login"] = True
            return jsonify({"response": "To view your transactions, please log in first. What is your 4-digit Account ID?"})
            
        transactions = database.get_recent_transactions(session.get("account_id"))
        if not transactions:
            response = "You have no recent transactions."
        else:
            response = "Here are your recent transactions:<br>"
            for amount, t_type, date in transactions:
                response += f"- {date}: {t_type} of ${amount:.2f}<br>"
                
    elif tag == "logout":
        session.clear()
        response = "You have been successfully logged out."
        
    return jsonify({"response": response})

def handle_login(user_message):
    if "login_step" not in session:
        # User just entered account ID
        try:
            account_id = int(user_message.strip())
            session["login_step"] = "pin"
            session["temp_account_id"] = account_id
            return jsonify({"response": "Thank you. Now, please enter your PIN:"})
        except ValueError:
            return jsonify({"response": "Invalid Account ID. Please enter a valid number (e.g. 1001):"})
            
    elif session["login_step"] == "pin":
        pin = user_message.strip()
        account_id = session.get("temp_account_id")
        
        user_name = database.authenticate(account_id, pin)
        
        if user_name:
            session["logged_in"] = True
            session["account_id"] = account_id
            session["user_name"] = user_name
            
            # Clear temp login data
            session.pop("awaiting_login", None)
            session.pop("login_step", None)
            session.pop("temp_account_id", None)
            
            return jsonify({"response": f"Login successful! Welcome back, {user_name}. How can I help you today?"})
        else:
            # Clear temp login data on failure
            session.pop("awaiting_login", None)
            session.pop("login_step", None)
            session.pop("temp_account_id", None)
            
            return jsonify({"response": "Authentication failed. Invalid Account ID or PIN. Please try asking your request again."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
