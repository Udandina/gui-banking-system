# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import database as db

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banking System")
        self.geometry("600x400")
        self.show_login()

    def show_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Login").pack()
        tk.Label(self, text="Account Number").pack()
        self.acc_entry = tk.Entry(self)
        self.acc_entry.pack()
        tk.Label(self, text="PIN").pack()
        self.pin_entry = tk.Entry(self, show="*")
        self.pin_entry.pack()
        tk.Button(self, text="Login", command=self.login).pack()
        tk.Button(self, text="Create Account", command=self.show_create_account).pack()
        tk.Button(self, text="Admin Login", command=self.show_admin_login).pack()

    def login(self):
        acc = self.acc_entry.get()
        pin = self.pin_entry.get()
        user_id = db.validate_login(acc, pin)
        if user_id:
            self.user_id = user_id
            self.acc_number = acc
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_create_account(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Create Account").pack()
        tk.Label(self, text="Full Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        tk.Label(self, text="PIN (4 digits)").pack()
        self.new_pin_entry = tk.Entry(self, show="*")
        self.new_pin_entry.pack()
        tk.Button(self, text="Create", command=self.create_acc).pack()
        tk.Button(self, text="Back", command=self.show_login).pack()

    def create_acc(self):
        name = self.name_entry.get()
        pin = self.new_pin_entry.get()
        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN must be 4 digits")
            return
        acc_num = db.create_account(name, pin)
        messagebox.showinfo("Success", f"Account created: {acc_num}")
        self.show_login()

    def show_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()
        balance = db.get_balance(self.user_id)
        tk.Label(self, text=f"Welcome, Balance: ₦{balance:.2f}").pack()
        tk.Button(self, text="Deposit", command=self.show_deposit).pack()
        tk.Button(self, text="Withdraw", command=self.show_withdraw).pack()
        tk.Button(self, text="Transfer", command=self.show_transfer).pack()
        tk.Button(self, text="History", command=self.show_history).pack()
        tk.Button(self, text="Logout", command=self.show_login).pack()

    def show_deposit(self):
        self.amount_window("Deposit", db.deposit)

    def show_withdraw(self):
        self.amount_window("Withdraw", db.withdraw)

    def amount_window(self, title, func):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=title).pack()
        tk.Label(self, text="Amount").pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()
        tk.Button(self, text="Submit", command=lambda: self.do_amount(func)).pack()
        tk.Button(self, text="Back", command=self.show_dashboard).pack()

    def do_amount(self, func):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid amount")
            return
        if func == db.withdraw:
            success = func(self.user_id, amount)
        else:
            func(self.user_id, amount)
            success = True
        if success:
            messagebox.showinfo("Success", "Operation successful")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Insufficient balance")

    def show_transfer(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Transfer").pack()
        tk.Label(self, text="To Account Number").pack()
        self.to_acc_entry = tk.Entry(self)
        self.to_acc_entry.pack()
        tk.Label(self, text="Amount").pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()
        tk.Button(self, text="Transfer", command=self.do_transfer).pack()
        tk.Button(self, text="Back", command=self.show_dashboard).pack()

    def do_transfer(self):
        to_acc = self.to_acc_entry.get()
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid amount")
            return
        if db.transfer(self.user_id, to_acc, amount):
            messagebox.showinfo("Success", "Transfer successful")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Transfer failed (insufficient balance or invalid account)")

    def show_history(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Transaction History").pack()
        tree = ttk.Treeview(self, columns=("Type", "Amount", "Other Account", "Time"), show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Other Account", text="Other Account")
        tree.heading("Time", text="Time")
        history = db.get_transaction_history(self.user_id)
        for trans in history:
            typ, amt, other_acc, ts = trans
            if other_acc is None:
                other_acc = ""
            if typ == 'transfer_out':
                typ = 'Transfer Out'
            elif typ == 'transfer_in':
                typ = 'Transfer In'
            tree.insert("", "end", values=(typ, f"₦{amt:.2f}", other_acc, ts))
        tree.pack(expand=True, fill='both')
        tk.Button(self, text="Back", command=self.show_dashboard).pack()

    def show_admin_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Admin Login").pack()
        tk.Label(self, text="PIN").pack()
        self.admin_pin_entry = tk.Entry(self, show="*")
        self.admin_pin_entry.pack()
        tk.Button(self, text="Login", command=self.admin_login_func).pack()
        tk.Button(self, text="Back", command=self.show_login).pack()

    def admin_login_func(self):
        pin = self.admin_pin_entry.get()
        if db.admin_login(pin):
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin PIN")

    def show_admin_panel(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Admin Panel").pack()
        tk.Button(self, text="View All Accounts", command=self.view_all_accounts).pack()
        tk.Button(self, text="Reset PIN", command=self.show_reset_pin).pack()
        tk.Button(self, text="Remove Account", command=self.show_remove_account).pack()
        tk.Button(self, text="Logout", command=self.show_login).pack()

    def view_all_accounts(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="All Accounts").pack()
        tree = ttk.Treeview(self, columns=("Acc Num", "Name", "Balance"), show="headings")
        tree.heading("Acc Num", text="Acc Num")
        tree.heading("Name", text="Name")
        tree.heading("Balance", text="Balance")
        accounts = db.get_all_accounts()
        for acc in accounts:
            acc_num, name, balance = acc
            tree.insert("", "end", values=(acc_num, name, f"₦{balance:.2f}"))
        tree.pack(expand=True, fill='both')
        tk.Button(self, text="Back", command=self.show_admin_panel).pack()

    def show_reset_pin(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Reset PIN").pack()
        tk.Label(self, text="Account Number").pack()
        self.reset_acc_entry = tk.Entry(self)
        self.reset_acc_entry.pack()
        tk.Label(self, text="New PIN (4 digits)").pack()
        self.reset_pin_entry = tk.Entry(self, show="*")
        self.reset_pin_entry.pack()
        tk.Button(self, text="Reset", command=self.do_reset_pin).pack()
        tk.Button(self, text="Back", command=self.show_admin_panel).pack()

    def do_reset_pin(self):
        acc = self.reset_acc_entry.get()
        pin = self.reset_pin_entry.get()
        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN must be 4 digits")
            return
        db.reset_pin(acc, pin)
        messagebox.showinfo("Success", "PIN reset")
        self.show_admin_panel()

    def show_remove_account(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Remove Account").pack()
        tk.Label(self, text="Account Number").pack()
        self.remove_acc_entry = tk.Entry(self)
        self.remove_acc_entry.pack()
        tk.Button(self, text="Remove", command=self.do_remove_account).pack()
        tk.Button(self, text="Back", command=self.show_admin_panel).pack()

    def do_remove_account(self):
        acc = self.remove_acc_entry.get()
        db.remove_account(acc)
        messagebox.showinfo("Success", "Account removed")
        self.show_admin_panel()