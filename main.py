# main.py
import database as db
import gui

if __name__ == "__main__":
    db.create_tables()
    app = gui.BankApp()
    app.mainloop()