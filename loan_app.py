import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from loan_manager import LoanManagementSystem
from datetime import datetime
import shutil
import os

class LoanApp:
    def __init__(self, root):
        self.system = LoanManagementSystem()
        self.root = root
        self.root.title("Offline Loan Management System")
        self.root.state('zoomed')  # Maximize window
        self.root.configure(bg='#F0F0F0')

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')

        # Define colors
        BG_COLOR = '#F0F0F0'
        TEXT_COLOR = '#333333'
        PRIMARY_COLOR = '#0078D7'
        WHITE = '#FFFFFF'
        BORDER_COLOR = '#CCCCCC'

        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=('Arial', 11))
        style.configure('TNotebook', background=BG_COLOR, tabmargins=0)
        style.configure('TNotebook.Tab', background='#E0E0E0', foreground=TEXT_COLOR, padding=[10, 5], font=('Arial', 12))
        style.map('TNotebook.Tab', background=[('selected', PRIMARY_COLOR)], foreground=[('selected', WHITE)])
        style.configure('TButton', background=PRIMARY_COLOR, foreground=WHITE, font=('Arial', 11, 'bold'), borderwidth=0)
        style.map('TButton', background=[('active', '#005A9E')])
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Arial', 11))
        style.configure('TEntry', fieldbackground=WHITE, foreground=TEXT_COLOR, bordercolor=BORDER_COLOR, insertcolor=TEXT_COLOR)
        style.configure('TCombobox', fieldbackground=WHITE, foreground=TEXT_COLOR, bordercolor=BORDER_COLOR, arrowcolor=PRIMARY_COLOR)
        style.map('TCombobox', fieldbackground=[('readonly', WHITE)])
        
        # Create notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Tabs
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.borrower_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.borrower_frame, text="Borrowers")
        self.loan_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.loan_frame, text="Loans")
        self.payment_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.payment_frame, text="Payments")
        self.report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.report_frame, text="Reports")
        
        self.setup_dashboard()
        self.setup_borrower_tab()
        self.setup_loan_tab()
        self.setup_payment_tab()
        self.setup_report_tab()

    def setup_dashboard(self):
        self.dashboard_content = ttk.Frame(self.dashboard_frame)
        self.dashboard_content.pack(pady=20, padx=20, fill='both', expand=True)
        self.update_dashboard()

    def update_dashboard(self):
        # Clear existing content
        for widget in self.dashboard_content.winfo_children():
            widget.destroy()
        
        data = self.system.get_dashboard_data()
        
        # Metrics frame
        metrics_frame = ttk.Frame(self.dashboard_content)
        metrics_frame.pack(pady=10, fill='x')
        
        ttk.Label(metrics_frame, text=f"Total Loans: {data['total_loans']}", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady=5)
        ttk.Label(metrics_frame, text=f"Total Amount: ₱{data['total_amount']:.2f}", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=20, pady=5)
        ttk.Label(metrics_frame, text=f"Active Loans: {data['active_loans']}", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=20, pady=5)
        ttk.Label(metrics_frame, text=f"Overdue Loans: {data['overdue_loans']}", font=("Arial", 14, "bold")).grid(row=0, column=3, padx=20, pady=5)
        
        # Charts frame
        charts_frame = ttk.Frame(self.dashboard_content)
        charts_frame.pack(pady=20, fill='both', expand=True)
        
        # Status pie chart
        status_df = pd.DataFrame(data['status_data'], columns=['Status', 'Count'])
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.pie(status_df['Count'], labels=status_df['Status'], autopct='%1.1f%%', colors=['#0078D7', '#FF5722', '#2196F3'])
        ax1.set_title("Loan Status Distribution", color='#333333')
        fig1.set_facecolor('#F0F0F0')
        
        canvas1 = FigureCanvasTkAgg(fig1, master=charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=20)
        
        # Amount distribution histogram
        if data['amounts']:
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.hist(data['amounts'], bins=10, color='#0078D7', edgecolor='white')
            ax2.set_title("Loan Amount Distribution", color='#333333')
            ax2.set_xlabel("Amount (₱)", color='#333333')
            ax2.set_ylabel("Count", color='#333333')
            fig2.set_facecolor('#F0F0F0')
            ax2.set_facecolor('#FFFFFF')
            ax2.tick_params(colors='#333333')
            
            canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=0, column=1, padx=20)

    def setup_borrower_tab(self):
        form_frame = ttk.Frame(self.borrower_frame)
        form_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(form_frame, text="Full Name").grid(row=0, column=0, padx=5, pady=5)
        self.full_name_entry = ttk.Entry(form_frame)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contact").grid(row=1, column=0, padx=5, pady=5)
        self.contact_entry = ttk.Entry(form_frame)
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Address").grid(row=3, column=0, padx=5, pady=5)
        self.address_entry = ttk.Entry(form_frame)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="ID Type").grid(row=4, column=0, padx=5, pady=5)
        self.id_type_entry = ttk.Entry(form_frame)
        self.id_type_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="ID Number").grid(row=5, column=0, padx=5, pady=5)
        self.id_number_entry = ttk.Entry(form_frame)
        self.id_number_entry.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Borrower", command=self.add_borrower).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Search
        search_frame = ttk.Frame(self.borrower_frame)
        search_frame.pack(pady=10, fill='x')
        ttk.Label(search_frame, text="Search by Name/ID").grid(row=0, column=0, padx=5, pady=5)
        self.borrower_search_entry = ttk.Entry(search_frame)
        self.borrower_search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_borrowers).grid(row=0, column=2, padx=5, pady=5)
        
        # Borrower list
        self.borrower_listbox = tk.Listbox(self.borrower_frame, width=80, bg='#3C3C3C', fg='white', font=('Arial', 11))
        self.borrower_listbox.pack(pady=10, padx=10, fill='both', expand=True)
        self.update_borrower_list()

    def setup_loan_tab(self):
        form_frame = ttk.Frame(self.loan_frame)
        form_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(form_frame, text="Borrower Name").grid(row=0, column=0, padx=5, pady=5)
        self.borrower_name_var = tk.StringVar()
        self.borrower_name_dropdown = ttk.Combobox(form_frame, textvariable=self.borrower_name_var, values=self.system.get_borrower_names())
        self.borrower_name_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Loan Amount").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Interest Rate (%)").grid(row=2, column=0, padx=5, pady=5)
        self.interest_entry = ttk.Entry(form_frame)
        self.interest_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Term (Months)").grid(row=3, column=0, padx=5, pady=5)
        self.term_entry = ttk.Entry(form_frame)
        self.term_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Loan", command=self.add_loan).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Search
        search_frame = ttk.Frame(self.loan_frame)
        search_frame.pack(pady=10, fill='x')
        ttk.Label(search_frame, text="Search by Name/Loan ID").grid(row=0, column=0, padx=5, pady=5)
        self.loan_search_entry = ttk.Entry(search_frame)
        self.loan_search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_loans).grid(row=0, column=2, padx=5, pady=5)
        
        # Loan list
        self.loan_listbox = tk.Listbox(self.loan_frame, width=80, bg='#3C3C3C', fg='white', font=('Arial', 11))
        self.loan_listbox.pack(pady=10, padx=10, fill='both', expand=True)
        self.update_loan_list()

    def setup_payment_tab(self):
        form_frame = ttk.Frame(self.payment_frame)
        form_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(form_frame, text="Borrower Name").grid(row=0, column=0, padx=5, pady=5)
        self.payment_name_var = tk.StringVar()
        self.payment_name_dropdown = ttk.Combobox(form_frame, textvariable=self.payment_name_var, values=self.system.get_borrower_names())
        self.payment_name_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Loan ID").grid(row=1, column=0, padx=5, pady=5)
        self.payment_loan_id_entry = ttk.Entry(form_frame)
        self.payment_loan_id_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Payment Amount").grid(row=2, column=0, padx=5, pady=5)
        self.payment_amount_entry = ttk.Entry(form_frame)
        self.payment_amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Record Payment", command=self.record_payment).grid(row=3, column=0, columnspan=2, pady=10)

    def setup_report_tab(self):
        report_frame = ttk.Frame(self.report_frame)
        report_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Button(report_frame, text="Export Loan Report to CSV", command=self.export_report).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(report_frame, text="Backup Database", command=self.backup_database).grid(row=0, column=1, padx=5, pady=5)

    def add_borrower(self):
        full_name = self.full_name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        id_type = self.id_type_entry.get().strip()
        id_number = self.id_number_entry.get().strip()
        
        if not full_name:
            messagebox.showerror("Error", "Full Name is required")
            return
        if id_number and not id_type:
            messagebox.showerror("Error", "ID Type is required if ID Number is provided")
            return
        
        borrower_id = self.system.add_borrower(full_name, contact, email, address, id_type, id_number)
        if borrower_id:
            messagebox.showinfo("Success", f"Borrower added with ID: {borrower_id}")
            self.update_borrower_list()
            self.update_dropdowns()
            self.update_dashboard()
        else:
            messagebox.showerror("Error", "Failed to add borrower")

    def add_loan(self):
        try:
            full_name = self.borrower_name_var.get()
            borrower = self.system.get_borrower_by_name(full_name)
            if not borrower:
                messagebox.showerror("Error", "Select a valid borrower")
                return
            borrower_id = borrower[0]
            amount = float(self.amount_entry.get())
            interest_rate = float(self.interest_entry.get())
            term_months = int(self.term_entry.get())
            if amount <= 0 or interest_rate < 0 or term_months <= 0:
                messagebox.showerror("Error", "Invalid numeric values")
                return
            start_date = datetime.now().strftime("%Y-%m-%d")
            loan_id = self.system.add_loan(borrower_id, amount, interest_rate, term_months, start_date)
            if loan_id:
                messagebox.showinfo("Success", f"Loan added with ID: {loan_id}")
                self.update_loan_list()
                self.update_dashboard()
            else:
                messagebox.showerror("Error", "Failed to add loan")
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def record_payment(self):
        try:
            full_name = self.payment_name_var.get()
            borrower = self.system.get_borrower_by_name(full_name)
            if not borrower:
                messagebox.showerror("Error", "Select a valid borrower")
                return
            loan_id = int(self.payment_loan_id_entry.get())
            amount = float(self.payment_amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Payment amount must be positive")
                return
            payment_date = datetime.now().strftime("%Y-%m-%d")
            result = self.system.record_payment(loan_id, amount, payment_date)
            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", f"Payment recorded. New balance: ₱{result:.2f}")
                self.update_loan_list()
                self.update_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def search_borrowers(self):
        query = self.borrower_search_entry.get().strip()
        self.borrower_listbox.delete(0, tk.END)
        for borrower in self.system.search_borrowers(query):
            id_number = borrower[5] if len(borrower) > 5 else "N/A"
            self.borrower_listbox.insert(tk.END, f"ID: {borrower[0]} | Name: {borrower[1]} | Contact: {borrower[2] or 'N/A'} | Email: {borrower[3] or 'N/A'} | ID: {id_number}")

    def search_loans(self):
        query = self.loan_search_entry.get().strip()
        self.loan_listbox.delete(0, tk.END)
        for loan in self.system.search_loans(query):
            self.loan_listbox.insert(tk.END, f"ID: {loan[0]} | Name: {loan[1]} | Amount: ₱{loan[2]:.2f} | Status: {loan[6]}")

    def update_borrower_list(self):
        self.borrower_listbox.delete(0, tk.END)
        for borrower in self.system.get_all_borrowers():
            id_number = borrower[5] if len(borrower) > 5 else "N/A"
            self.borrower_listbox.insert(tk.END, f"ID: {borrower[0]} | Name: {borrower[1]} | Contact: {borrower[2] or 'N/A'} | Email: {borrower[3] or 'N/A'} | ID: {id_number}")

    def update_loan_list(self):
        self.loan_listbox.delete(0, tk.END)
        for loan in self.system.get_all_loans():
            self.loan_listbox.insert(tk.END, f"ID: {loan[0]} | Name: {loan[1]} | Amount: ₱{loan[2]:.2f} | Status: {loan[6]}")

    def update_dropdowns(self):
        names = self.system.get_borrower_names()
        self.borrower_name_dropdown['values'] = names
        self.payment_name_dropdown['values'] = names

    def export_report(self):
        if self.system.export_loan_report():
            messagebox.showinfo("Success", "Loan report exported to loan_report.csv")
        else:
            messagebox.showerror("Error", "Failed to export report")

    def backup_database(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])
        if file_path:
            shutil.copy('loan_management.db', file_path)
            messagebox.showinfo("Success", f"Database backed up to {file_path}")

    def __del__(self):
        self.system.close()

if __name__ == "__main__":
    from database_setup import create_database
    create_database()
    root = tk.Tk()
    app = LoanApp(root)
    root.mainloop()