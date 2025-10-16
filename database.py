# database.py
import sqlite3
import hashlib
import time
import random

def create_connection():
    conn = sqlite3.connect('bank.db')
    return conn

def create_tables():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (id INTEGER PRIMARY KEY,
                  account_number TEXT UNIQUE,
                  full_name TEXT,
                  pin_hash TEXT,
                  balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY,
                  account_id INTEGER,
                  type TEXT,
                  amount REAL,
                  other_account TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def create_account(full_name, pin):
    conn = create_connection()
    c = conn.cursor()
    account_number = str(int(time.time())) + str(random.randint(1000, 9999))
    pin_hash = hash_pin(pin)
    c.execute("INSERT INTO accounts (account_number, full_name, pin_hash) VALUES (?, ?, ?)",
              (account_number, full_name, pin_hash))
    conn.commit()
    account_id = c.lastrowid
    conn.close()
    return account_number

def validate_login(account_number, pin):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT id, pin_hash FROM accounts WHERE account_number = ?", (account_number,))
    result = c.fetchone()
    conn.close()
    if result:
        user_id, pin_hash = result
        if hash_pin(pin) == pin_hash:
            return user_id
    return None

def get_balance(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT balance FROM accounts WHERE id = ?", (user_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance

def deposit(user_id, amount):
    conn = create_connection()
    c = conn.cursor()
    c.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, user_id))
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (?, 'deposit', ?, ?)",
              (user_id, amount, timestamp))
    conn.commit()
    conn.close()

def withdraw(user_id, amount):
    balance = get_balance(user_id)
    if balance >= amount:
        conn = create_connection()
        c = conn.cursor()
        c.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, user_id))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (?, 'withdraw', ?, ?)",
                  (user_id, amount, timestamp))
        conn.commit()
        conn.close()
        return True
    return False

def transfer(from_id, to_account_number, amount):
    balance = get_balance(from_id)
    if balance >= amount:
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM accounts WHERE account_number = ?", (to_account_number,))
        to_result = c.fetchone()
        if to_result:
            to_id = to_result[0]
            c.execute("SELECT account_number FROM accounts WHERE id = ?", (from_id,))
            from_account_number = c.fetchone()[0]
            c.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
            c.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO transactions (account_id, type, amount, other_account, timestamp) VALUES (?, 'transfer_out', ?, ?, ?)",
                      (from_id, amount, to_account_number, timestamp))
            c.execute("INSERT INTO transactions (account_id, type, amount, other_account, timestamp) VALUES (?, 'transfer_in', ?, ?, ?)",
                      (to_id, amount, from_account_number, timestamp))
            conn.commit()
            conn.close()
            return True
    return False

def get_transaction_history(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT type, amount, other_account, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp DESC",
              (user_id,))
    history = c.fetchall()
    conn.close()
    return history

# Admin functions
ADMIN_PIN_HASH = hash_pin('1234')  # Default admin PIN: 1234

def admin_login(pin):
    return hash_pin(pin) == ADMIN_PIN_HASH

def get_all_accounts():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT account_number, full_name, balance FROM accounts")
    accounts = c.fetchall()
    conn.close()
    return accounts

def reset_pin(account_number, new_pin):
    conn = create_connection()
    c = conn.cursor()
    pin_hash = hash_pin(new_pin)
    c.execute("UPDATE accounts SET pin_hash = ? WHERE account_number = ?", (pin_hash, account_number))
    conn.commit()
    conn.close()

def remove_account(account_number):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE account_id = (SELECT id FROM accounts WHERE account_number = ?)", (account_number,))
    c.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
    conn.commit()
    conn.close()