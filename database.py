import sqlite3
import datetime

DB_NAME = "banking.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            account_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')
    
    # Create Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            amount REAL,
            type TEXT,
            date TEXT,
            FOREIGN KEY(account_id) REFERENCES users(account_id)
        )
    ''')
    
    # Check if we need to insert sample data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        print("Inserting sample users...")
        users = [
            (1001, "Alice Smith", "1234", 5000.50),
            (1002, "Bob Johnson", "5678", 250.75)
        ]
        cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)
        
        # Insert sample transactions
        now = datetime.datetime.now()
        transactions = [
            (1001, 1500.0, "Deposit", (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
            (1001, 50.0, "Withdrawal", (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
            (1002, 250.75, "Deposit", now.strftime("%Y-%m-%d %H:%M:%S"))
        ]
        cursor.executemany("INSERT INTO transactions (account_id, amount, type, date) VALUES (?, ?, ?, ?)", transactions)
    
    conn.commit()
    conn.close()

def authenticate(account_id, pin):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE account_id=? AND pin=?", (account_id, pin))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def get_balance(account_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE account_id=?", (account_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_recent_transactions(account_id, limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, type, date FROM transactions WHERE account_id=? ORDER BY date DESC LIMIT ?", (account_id, limit))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

if __name__ == "__main__":
    init_db()
    print("Database initialized with sample data.")
