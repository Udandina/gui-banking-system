Banking System Application
A Python-based banking system with a Tkinter GUI, SQLite database, and secure PIN validation using hashlib. The application supports user account management, banking transactions, and admin functionalities.
Features

Account Management:
Create accounts with full name, auto-generated account number, 4-digit PIN, and starting balance (₦0).
Data stored persistently in SQLite.


Secure Login:
Login using account number and PIN, validated with SHA-256 hashing.


Transactions:
Deposit funds.
Withdraw funds (prevents negative balance).
Transfer funds between accounts.
View balance and transaction history in a table.


Admin Mode:
Login with default PIN 1234.
View all accounts, reset user PINs, and remove accounts.



Requirements

Python 3.6 or higher.
Tkinter (usually included with Python).
Ubuntu/Debian: sudo apt-get install python3-tk
Fedora: sudo dnf install python3-tkinter
macOS/Windows: Typically included with Python.


SQLite (included with Python).

Installation

Clone or Download:

Download the project files or clone the repository.
Ensure the following files are in the project directory:
database.py
gui.py
main.py




Directory Structure:
banking_system/
├── database.py
├── gui.py
├── main.py
├── README.md


Run the Application:

Open a terminal and navigate to the project directory:cd path/to/banking_system


Run the main script:python main.py

orpython3 main.py





Usage

User Interface:

Login Screen: Log in with account number and PIN, create a new account, or access admin mode.
Create Account: Enter full name and a 4-digit PIN to generate an account number.
Dashboard: Perform deposits, withdrawals, transfers, or view transaction history.
Admin Mode: Log in with PIN 1234 to view all accounts, reset PINs, or remove accounts.


Database:

A bank.db SQLite file is created automatically to store accounts and transactions.



Notes

The default admin PIN is 1234. Modify ADMIN_PIN_HASH in database.py to change it (hash the new PIN using hash_pin).
Ensure write permissions in the project directory for bank.db.
Transaction history is displayed in a table with type, amount, other account (for transfers), and timestamp.

Troubleshooting

Tkinter not found: Install Tkinter using your package manager (see Requirements).
SQLite errors: Ensure directory permissions allow file creation.
GUI issues: Verify Python includes Tkinter and you're running in a graphical environment.
Check terminal for error messages if the application fails to run.

License
This project is for educational purposes and not licensed for commercial use.
