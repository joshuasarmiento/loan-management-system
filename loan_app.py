import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from loan_manager import LoanManagementSystem
from datetime import datetime
import shutil
import os
from PIL import Image, ImageTk

class LoanApp:
    def __init__(self, root, show_login_callback):
        self.system = LoanManagementSystem()
        self.root = root
        self.show_login_callback = show_login_callback
        self.root.title("Offline Loan Management System")
        self.root.state('zoomed')  # Maximize window
        self.root.configure(bg='#F0F0F0')

        # Helper function to load and resize icons
        def _load_icon(path, size=(64, 64)):
            try:
                img = Image.open(path)
                img = img.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except FileNotFoundError:
                messagebox.showwarning("Icon Warning", f"Icon not found: {path}")
                return None # Or return a default blank image

        # Load icons
        self.add_borrower_icon = _load_icon('icons/add_borrower.png')
        self.add_loan_icon = _load_icon('icons/add_loan.png')
        self.record_payment_icon = _load_icon('icons/record_payment.png')
        self.export_report_icon = _load_icon('icons/export_report.png')
        self.backup_db_icon = _load_icon('icons/backup_db.png')
        self.logout_icon = _load_icon('icons/logout.png')
        self.search_icon = _load_icon('icons/search.png')
        self.dashboard_icon = _load_icon('icons/dashboard.png')
        self.borrower_icon = _load_icon('icons/borrower.png')
        self.loan_icon = _load_icon('icons/loan.png')
        self.payment_icon = _load_icon('icons/payment.png')
        self.report_icon = _load_icon('icons/report.png')

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
        
        # Treeview styles
        style.configure('Treeview',
                        background=WHITE,
                        foreground=TEXT_COLOR,
                        rowheight=25,
                        fieldbackground=WHITE,
                        bordercolor=BORDER_COLOR,
                        borderwidth=1)
        style.map('Treeview', background=[('selected', PRIMARY_COLOR)])
        style.configure('Treeview.Heading',
                        font=('Arial', 11, 'bold'),
                        background=PRIMARY_COLOR,
                        foreground=WHITE,
                        relief='flat')
        style.map('Treeview.Heading',
                  background=[('active', '#005A9E')])

        # Custom style for shadow frames
        style.configure('Shadow.TFrame', background='#AAAAAA', relief='flat') # Darker background for shadow
        style.map('Shadow.TFrame', background=[('active', '#888888')])
        
        # Create main content frame
        self.main_content_frame = ttk.Frame(self.root)
        self.main_content_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Dictionary to hold different views
        self.views = {}

        # Setup individual view frames (initially hidden)
        self.dashboard_frame = ttk.Frame(self.main_content_frame)
        self.borrower_frame = ttk.Frame(self.main_content_frame)
        self.loan_frame = ttk.Frame(self.main_content_frame)
        self.payment_frame = ttk.Frame(self.main_content_frame)
        self.report_frame = ttk.Frame(self.main_content_frame)

        self.views["Dashboard"] = self.dashboard_frame
        self.views["Borrowers"] = self.borrower_frame
        self.views["Loans"] = self.loan_frame
        self.views["Payments"] = self.payment_frame
        self.views["Reports"] = self.report_frame

        # Create a persistent back button frame and button
        self.back_button_frame = ttk.Frame(self.root)
        self.back_button = ttk.Button(self.back_button_frame, text="Back to Main Menu", command=lambda: self.show_view("Main Menu"))
        self.back_button.pack(side=tk.LEFT)

        # Call setup methods for each view
        self.setup_dashboard()
        self.setup_borrower_tab()
        self.setup_loan_tab()
        self.setup_payment_tab()
        self.setup_report_tab()

        # Show the main menu initially
        self.setup_main_menu()
        self.show_view("Main Menu")

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
        ttk.Button(metrics_frame, text="Logout", command=self.logout, image=self.logout_icon, compound=tk.LEFT).grid(row=0, column=4, padx=20, pady=5)
        
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
        
        # Input fields arranged horizontally
        input_row1 = ttk.Frame(form_frame)
        input_row1.pack(fill='x', pady=2)
        ttk.Label(input_row1, text="Full Name").pack(side='left', padx=5, pady=5)
        self.full_name_entry = ttk.Entry(input_row1)
        self.full_name_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)
        
        ttk.Label(input_row1, text="Contact").pack(side='left', padx=5, pady=5)
        self.contact_entry = ttk.Entry(input_row1)
        self.contact_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)
        
        input_row2 = ttk.Frame(form_frame)
        input_row2.pack(fill='x', pady=2)
        ttk.Label(input_row2, text="Email").pack(side='left', padx=5, pady=5)
        self.email_entry = ttk.Entry(input_row2)
        self.email_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)
        
        ttk.Label(input_row2, text="Address").pack(side='left', padx=5, pady=5)
        self.address_entry = ttk.Entry(input_row2)
        self.address_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)
        
        input_row3 = ttk.Frame(form_frame)
        input_row3.pack(fill='x', pady=2)
        ttk.Label(input_row3, text="ID Type").pack(side='left', padx=5, pady=5)
        self.id_type_entry = ttk.Entry(input_row3)
        self.id_type_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)
        
        ttk.Label(input_row3, text="ID Number").pack(side='left', padx=5, pady=5)
        self.id_number_entry = ttk.Entry(input_row3)
        self.id_number_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Borrower", command=self.add_borrower, image=self.add_borrower_icon, compound=tk.LEFT).pack(pady=10)
        
        # Search
        search_frame = ttk.Frame(self.borrower_frame)
        search_frame.pack(pady=10, fill='x')
        ttk.Label(search_frame, text="Search by Name/ID").grid(row=0, column=0, padx=5, pady=5)
        self.borrower_search_entry = ttk.Entry(search_frame)
        self.borrower_search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_borrowers, image=self.search_icon, compound=tk.LEFT).grid(row=0, column=2, padx=5, pady=5)
        
        # Borrower list
        self.borrower_listbox = ttk.Treeview(self.borrower_frame, columns=("ID", "Full Name", "Contact", "Email", "Address", "ID Type", "ID Number"), show="headings")
        self.borrower_listbox.heading("ID", text="ID")
        self.borrower_listbox.heading("Full Name", text="Full Name")
        self.borrower_listbox.heading("Contact", text="Contact")
        self.borrower_listbox.heading("Email", text="Email")
        self.borrower_listbox.heading("Address", text="Address")
        self.borrower_listbox.heading("ID Type", text="ID Type")
        self.borrower_listbox.heading("ID Number", text="ID Number")
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
        
        ttk.Button(form_frame, text="Add Loan", command=self.add_loan, image=self.add_loan_icon, compound=tk.LEFT).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Search
        search_frame = ttk.Frame(self.loan_frame)
        search_frame.pack(pady=10, fill='x')
        ttk.Label(search_frame, text="Search by Name/Loan ID").grid(row=0, column=0, padx=5, pady=5)
        self.loan_search_entry = ttk.Entry(search_frame)
        self.loan_search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_loans, image=self.search_icon, compound=tk.LEFT).grid(row=0, column=2, padx=5, pady=5)
        
        # Loan list
        self.loan_listbox = ttk.Treeview(self.loan_frame, columns=("ID", "Borrower Name", "Amount", "Interest Rate", "Term", "Start Date", "Status", "Balance"), show="headings")
        self.loan_listbox.heading("ID", text="ID")
        self.loan_listbox.heading("Borrower Name", text="Borrower Name")
        self.loan_listbox.heading("Amount", text="Amount")
        self.loan_listbox.heading("Interest Rate", text="Interest Rate")
        self.loan_listbox.heading("Term", text="Term")
        self.loan_listbox.heading("Start Date", text="Start Date")
        self.loan_listbox.heading("Status", text="Status")
        self.loan_listbox.heading("Balance", text="Balance")
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
        
        ttk.Button(form_frame, text="Record Payment", command=self.record_payment, image=self.record_payment_icon, compound=tk.LEFT).grid(row=3, column=0, columnspan=2, pady=10)

    def setup_report_tab(self):
        report_frame = ttk.Frame(self.report_frame)
        report_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Button(report_frame, text="Export Loan Report to CSV", command=self.export_report, image=self.export_report_icon, compound=tk.LEFT).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(report_frame, text="Backup Database", command=self.backup_database, image=self.backup_db_icon, compound=tk.LEFT).grid(row=0, column=1, padx=5, pady=5)

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
            self.full_name_entry.delete(0, tk.END)
            self.contact_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            self.id_type_entry.delete(0, tk.END)
            self.id_number_entry.delete(0, tk.END)
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
                self.amount_entry.delete(0, tk.END)
                self.interest_entry.delete(0, tk.END)
                self.term_entry.delete(0, tk.END)
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
                self.payment_loan_id_entry.delete(0, tk.END)
                self.payment_amount_entry.delete(0, tk.END)
                self.update_loan_list()
                self.update_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def search_borrowers(self):
        query = self.borrower_search_entry.get().strip()
        for i in self.borrower_listbox.get_children():
            self.borrower_listbox.delete(i)
        for borrower in self.system.search_borrowers(query):
            self.borrower_listbox.insert('', tk.END, values=borrower)

    def search_loans(self):
        query = self.loan_search_entry.get().strip()
        for i in self.loan_listbox.get_children():
            self.loan_listbox.delete(i)
        for loan in self.system.search_loans(query):
            self.loan_listbox.insert('', tk.END, values=loan)

    def update_borrower_list(self):
        for i in self.borrower_listbox.get_children():
            self.borrower_listbox.delete(i)
        for borrower in self.system.get_all_borrowers():
            self.borrower_listbox.insert('', tk.END, values=borrower)

    def update_loan_list(self):
        for i in self.loan_listbox.get_children():
            self.loan_listbox.delete(i)
        for loan in self.system.get_all_loans():
            loan_id, borrower_name, amount, interest_rate, term_months, start_date, status = loan
            balance = self.system.get_loan_balance(loan_id) # Assuming this method exists or will be added
            self.loan_listbox.insert('', tk.END, values=(loan_id, borrower_name, amount, interest_rate, term_months, start_date, status, f"{balance:.2f}"))

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

    def logout(self):
        self.main_content_frame.pack_forget()  # Hide the main application content
        self.back_button_frame.pack_forget() # Hide the back button frame
        self.show_login_callback()  # Call the function to show the login window again

    def __del__(self):
        self.system.close()

    def setup_main_menu(self):
        self.main_menu_frame = ttk.Frame(self.main_content_frame)
        self.views["Main Menu"] = self.main_menu_frame

        menu_label = ttk.Label(self.main_menu_frame, text="Main Menu", font=("Arial", 24, "bold"))
        menu_label.grid(row=0, column=0, columnspan=3, pady=20) # Use grid instead of pack

        # Center the grid of buttons
        self.main_menu_frame.grid_rowconfigure(0, weight=1)
        self.main_menu_frame.grid_rowconfigure(1, weight=1)
        self.main_menu_frame.grid_columnconfigure(0, weight=1)
        self.main_menu_frame.grid_columnconfigure(1, weight=1)
        self.main_menu_frame.grid_columnconfigure(2, weight=1)

        # Dashboard Button
        dashboard_shadow_frame = ttk.Frame(self.main_menu_frame, style='Shadow.TFrame')
        dashboard_shadow_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # Adjusted row to 1
        dashboard_button = ttk.Button(dashboard_shadow_frame, text="Dashboard", image=self.dashboard_icon, compound=tk.TOP, command=lambda: self.show_view("Dashboard"))
        dashboard_button.pack(expand=True, fill='both', padx=5, pady=5)

        # Borrowers Button
        borrower_shadow_frame = ttk.Frame(self.main_menu_frame, style='Shadow.TFrame')
        borrower_shadow_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew") # Adjusted row to 1
        borrower_button = ttk.Button(borrower_shadow_frame, text="Borrowers", image=self.borrower_icon, compound=tk.TOP, command=lambda: self.show_view("Borrowers"))
        borrower_button.pack(expand=True, fill='both', padx=5, pady=5)

        # Loans Button
        loan_shadow_frame = ttk.Frame(self.main_menu_frame, style='Shadow.TFrame')
        loan_shadow_frame.grid(row=1, column=2, padx=20, pady=20, sticky="nsew") # Adjusted row to 1
        loan_button = ttk.Button(loan_shadow_frame, text="Loans", image=self.loan_icon, compound=tk.TOP, command=lambda: self.show_view("Loans"))
        loan_button.pack(expand=True, fill='both', padx=5, pady=5)

        # Payments Button
        payment_shadow_frame = ttk.Frame(self.main_menu_frame, style='Shadow.TFrame')
        payment_shadow_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew") # Adjusted row to 2
        payment_button = ttk.Button(payment_shadow_frame, text="Payments", image=self.payment_icon, compound=tk.TOP, command=lambda: self.show_view("Payments"))
        payment_button.pack(expand=True, fill='both', padx=5, pady=5)

        # Reports Button
        report_shadow_frame = ttk.Frame(self.main_menu_frame, style='Shadow.TFrame')
        report_shadow_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew") # Adjusted row to 2
        report_button = ttk.Button(report_shadow_frame, text="Reports", image=self.report_icon, compound=tk.TOP, command=lambda: self.show_view("Reports"))
        report_button.pack(expand=True, fill='both', padx=5, pady=5)

    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.pack_forget()

        # Show the requested view
        self.views[view_name].pack(fill='both', expand=True)

        # Manage back button visibility
        if view_name != "Main Menu":
            self.back_button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        else:
            self.back_button_frame.pack_forget()

if __name__ == "__main__":
    from database_setup import create_database
    create_database()
    root = tk.Tk()
    try:
        root.iconbitmap('app_icon.ico') # Set the application icon
    except tk.TclError:
        # Handle cases where the icon file is not found or is not a valid .ico file
        pass
    root.withdraw()  # Hide the main window initially
    
    login_successful = False
    login_window = None # Initialize login_window to None

    def authenticate(username, password):
        global login_successful
        if username == "admin" and password == "password":  # Hardcoded credentials
            login_successful = True
            messagebox.showinfo("Login Success", "Welcome to Loan Management System!")
            if login_window: # Check if login_window exists before destroying
                login_window.destroy()
            root.deiconify()  # Show the main window
            app = LoanApp(root, show_login_window)
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def show_login_window():
        global login_window
        if login_window is None or not login_window.winfo_exists(): # Create only if it doesn't exist or was destroyed
            login_window = tk.Toplevel(root)
            login_window.title("Login")
            login_window.geometry("300x150")
            login_window.resizable(False, False)
            login_window.protocol("WM_DELETE_WINDOW", root.quit) # Exit app if login window closed

            # Center the login window
            login_window.update_idletasks()
            x = root.winfo_x() + (root.winfo_width() // 2) - (login_window.winfo_width() // 2)
            y = root.winfo_y() + (root.winfo_height() // 2) - (login_window.winfo_height() // 2)
            login_window.geometry(f"+{x}+{y}")

            ttk.Label(login_window, text="Username:").pack(pady=5)
            username_entry = ttk.Entry(login_window)
            username_entry.pack(pady=5)
            username_entry.focus_set()

            ttk.Label(login_window, text="Password:").pack(pady=5)
            password_entry = ttk.Entry(login_window, show="*")
            password_entry.pack(pady=5)

            ttk.Button(login_window, text="Login", command=lambda: authenticate(username_entry.get(), password_entry.get())).pack(pady=10)
            
            # Bind <Return> key to login
            login_window.bind('<Return>', lambda event=None: authenticate(username_entry.get(), password_entry.get()))
        else:
            login_window.deiconify() # Just show it if it already exists

    show_login_window()
    root.mainloop() # Keep the root mainloop running for the login window to function properly