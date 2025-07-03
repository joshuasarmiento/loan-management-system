# Offline Loan Management System

## Overview

This is an offline loan management system designed to manage borrowers, loans, and payments. It features a modern dashboard with metrics and charts, built using Python, SQLite, and Tkinter. The system runs locally without requiring an internet connection.

## Features

- **Borrower Management**: Add and view borrowers with Full Name, Contact, Email, Address, ID Type, and ID Number.
- **Loan Management**: Create and track loans with borrower selection via dropdown, amount, interest rate, and term.
- **Payment Tracking**: Record payments with borrower selection via dropdown and update loan balances.
- **Dashboard**: Displays total loans, total amount, active/overdue loans, and charts (loan status and amount distribution).
- **Reports**: Export loan summaries to CSV and backup the database.
- **Search**: Search borrowers by name/ID and loans by name/loan ID.
- **Offline**: All data is stored locally in an SQLite database.

## Installation

Follow these steps to install and run the system on a Windows, macOS, or Linux computer.

### Prerequisites

- A computer with at least 4GB RAM and 500MB free disk space.
- No internet connection is required after installation for the executable version.
- For source code usage, Python 3.8+ and specific libraries are required.

### Option 1: Using the Executable (Recommended)

1. **Extract the Package**:
   - Unzip `loan_management_system.zip` to a folder (e.g., `C:\LoanManagement` on Windows or `~/LoanManagement` on macOS/Linux).
2. **Run the Application**:
   - Navigate to the extracted folder.
   - Double-click `loan_app.exe` (Windows) or run `./loan_app` (macOS/Linux) from the terminal.
   - The application will create `loan_management.db` automatically if it doesn't exist.
3. **Ensure Database File**:
   - Keep `loan_management.db` in the same folder as the executable.
   - Do not delete or move this file, as it stores all data.

### Option 2: Running from Source Code

For users with Python installed:

1. **Install Python**:
   - Download and install Python 3.8 or later from [python.org](https://www.python.org/downloads/).
   - Ensure `pip` is included (checked by default during installation).
2. **Install Dependencies**:
   - Requires `matplotlib`, `pandas`, and `numpy`.
   - If the client machine has internet access, run:
     ```bash
     pip install matplotlib pandas
     ```
   - For offline installation, use the provided `dependencies` folder:
     ```bash
     pip install dependencies/matplotlib-*.whl
     pip install dependencies/pandas-*.whl
     pip install dependencies/numpy-*.whl
     ```
     Contact the provider if these files are missing.
3. **Run the Application**:
   - Navigate to the folder containing `loan_app.py`.
   - Run:
     ```bash
     python loan_app.py
     ```
   - The application will start, and `loan_management.db` will be created if it doesn't exist.

### Notes

- If you encounter `ModuleNotFoundError: No module named 'matplotlib'`, ensure `matplotlib` and `pandas` are installed (see above).
- On Windows, you may need the Microsoft Visual C++ Redistributable (available at [microsoft.com](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)).
- On macOS/Linux, grant execution permissions to the executable if needed:
  ```bash
  chmod +x loan_app
  ```

## Usage

1. **Launch the Application**:
   - Open the application using the executable or source code method.
2. **Navigate Tabs**:
   - **Dashboard**: View metrics (total loans, total amount, active/overdue loans) and charts (status and amount distribution).
   - **Borrowers**: Add borrowers (Full Name required) and search by name/ID.
   - **Loans**: Add loans by selecting a borrower from the dropdown, entering amount, interest rate, and term. Search by name/loan ID.
   - **Payments**: Record payments by selecting a borrower and entering loan ID and amount.
   - **Reports**: Export loan reports to CSV or backup the database.
3. **Example Workflow**:
   - Add a borrower (e.g., Full Name: John Doe, Contact: 123-456-7890, Email: john@example.com, ID Type: Passport, ID Number: 123456).
   - Add a loan (e.g., Borrower: John Doe, Amount: 10000, Interest: 5%, Term: 12 months).
   - Record a payment (e.g., Borrower: John Doe, Loan ID: 1, Amount: 1000).
   - Check the dashboard for updated metrics and charts.
   - Export a report or backup the database from the Reports tab.
4. **Data Storage**:
   - All data is stored in `loan_management.db`.
   - Back up this file regularly using the Reports tab.

## Troubleshooting

- **Application Won't Start**:
   - Ensure `loan_management.db` is in the same folder as the executable.
   - For source code, verify Python, `matplotlib`, and `pandas` are installed.
- **ModuleNotFoundError**:
   - Install missing libraries as described in Installation.
- **Invalid Input Errors**:
   - Ensure numeric fields (e.g., Amount, Loan ID) contain valid numbers.
   - Borrower must be selected from the dropdown.
- **Contact Support**:
   - Contact [your support email or phone number].

## Security

- Data is stored in `loan_management.db`. Ensure your computer is secure (e.g., use antivirus, restrict access).
- Use the Reports tab to back up `loan_management.db` to a secure location (e.g., USB drive).
- Consider encrypting the database file for sensitive data.

## System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+ recommended).
- **Disk Space**: ~500MB for executable and database.
- **Python** (for source code): Python 3.8+ with `matplotlib`, `pandas`, `numpy`.

## Notes

- Designed for small to medium-sized loan portfolios.
- Performance for large datasets depends on computer specifications.
- Do not modify or delete `loan_management.db` without a backup.