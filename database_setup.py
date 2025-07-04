import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect('loan_management.db')
    cursor = conn.cursor()
    
    # Create Borrowers table with updated fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowers (
            borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            address TEXT,
            id_type TEXT,
            id_number TEXT
        )
    ''')
    
    # Create Loans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            borrower_id INTEGER,
            amount REAL NOT NULL,
            interest_rate REAL NOT NULL,
            term_months INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id)
        )
    ''')
    
    # Create Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER,
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL,
            balance_after_payment REAL NOT NULL,
            FOREIGN KEY (loan_id) REFERENCES loans (loan_id)
        )
    ''')
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')

    # Add default admin user if not exists
    default_username = "admin"
    default_password = "password"
    hashed_password = hashlib.sha256(default_password.encode()).hexdigest()

    cursor.execute("SELECT * FROM users WHERE username = ?", (default_username,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (default_username, hashed_password))
        print(f"Default user '{default_username}' added.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()