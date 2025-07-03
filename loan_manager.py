import sqlite3
from datetime import datetime, timedelta
import pandas as pd

class LoanManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect('loan_management.db')
        self.cursor = self.conn.cursor()

    def add_borrower(self, full_name, contact, email, address, id_type, id_number):
        try:
            self.cursor.execute('INSERT INTO borrowers (full_name, contact, email, address, id_type, id_number) '
                              'VALUES (?, ?, ?, ?, ?, ?)',
                              (full_name, contact, email, address, id_type, id_number))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def add_loan(self, borrower_id, amount, interest_rate, term_months, start_date):
        try:
            status = "Active"
            self.cursor.execute('INSERT INTO loans (borrower_id, amount, interest_rate, term_months, start_date, status) '
                              'VALUES (?, ?, ?, ?, ?, ?)',
                              (borrower_id, amount, interest_rate, term_months, start_date, status))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def record_payment(self, loan_id, amount, payment_date):
        try:
            self.cursor.execute('SELECT amount, interest_rate, term_months, start_date FROM loans WHERE loan_id = ?', (loan_id,))
            loan = self.cursor.fetchone()
            if not loan:
                return "Loan not found"
            
            self.cursor.execute('SELECT SUM(amount) FROM payments WHERE loan_id = ?', (loan_id,))
            total_paid = self.cursor.fetchone()[0] or 0
            new_balance = loan[0] - total_paid - amount
            
            self.cursor.execute('INSERT INTO payments (loan_id, amount, payment_date, balance_after_payment) '
                              'VALUES (?, ?, ?, ?)', (loan_id, amount, payment_date, new_balance))
            
            status = "Paid" if new_balance <= 0 else "Active"
            start_date = datetime.strptime(loan[3], "%Y-%m-%d")
            if (datetime.now() - start_date).days > 30 and new_balance > 0:
                status = "Overdue"
            self.cursor.execute('UPDATE loans SET status = ? WHERE loan_id = ?', (status, loan_id))
            
            self.conn.commit()
            return new_balance
        except sqlite3.Error:
            return None

    def get_loan_summary(self, loan_id):
        self.cursor.execute('SELECT * FROM loans WHERE loan_id = ?', (loan_id,))
        loan = self.cursor.fetchone()
        self.cursor.execute('SELECT * FROM payments WHERE loan_id = ?', (loan_id,))
        payments = self.cursor.fetchall()
        return {"loan": loan, "payments": payments}

    def get_dashboard_data(self):
        self.cursor.execute('SELECT COUNT(*) FROM loans')
        total_loans = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT SUM(amount) FROM loans')
        total_amount = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute('SELECT COUNT(*) FROM loans WHERE status = "Active"')
        active_loans = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM loans WHERE status = "Overdue"')
        overdue_loans = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT status, COUNT(*) FROM loans GROUP BY status')
        status_data = self.cursor.fetchall()
        
        self.cursor.execute('SELECT amount FROM loans')
        amounts = [row[0] for row in self.cursor.fetchall()]
        
        return {
            "total_loans": total_loans,
            "total_amount": total_amount,
            "active_loans": active_loans,
            "overdue_loans": overdue_loans,
            "status_data": status_data,
            "amounts": amounts
        }

    def get_all_borrowers(self):
        self.cursor.execute('SELECT * FROM borrowers')
        return self.cursor.fetchall()

    def get_all_loans(self):
        self.cursor.execute('SELECT l.loan_id, b.full_name, l.amount, l.interest_rate, l.term_months, l.start_date, l.status '
                          'FROM loans l JOIN borrowers b ON l.borrower_id = b.borrower_id')
        return self.cursor.fetchall()

    def search_borrowers(self, query):
        self.cursor.execute('SELECT * FROM borrowers WHERE full_name LIKE ? OR id_number LIKE ?',
                          (f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()

    def search_loans(self, query):
        self.cursor.execute('SELECT l.loan_id, b.full_name, l.amount, l.interest_rate, l.term_months, l.start_date, l.status '
                          'FROM loans l JOIN borrowers b ON l.borrower_id = b.borrower_id '
                          'WHERE b.full_name LIKE ? OR l.loan_id LIKE ?',
                          (f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()

    def get_borrower_by_name(self, full_name):
        self.cursor.execute('SELECT borrower_id FROM borrowers WHERE full_name = ?', (full_name,))
        return self.cursor.fetchone()

    def get_borrower_names(self):
        self.cursor.execute('SELECT full_name FROM borrowers')
        return [row[0] for row in self.cursor.fetchall()]

    def export_loan_report(self):
        loans = pd.read_sql_query('SELECT l.loan_id, b.full_name, l.amount, l.interest_rate, l.term_months, l.start_date, l.status '
                                 'FROM loans l JOIN borrowers b ON l.borrower_id = b.borrower_id', self.conn)
        loans.to_csv('loan_report.csv', index=False)
        return True

    def close(self):
        self.conn.close()