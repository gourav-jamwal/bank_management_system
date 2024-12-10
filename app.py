import tkinter as tk
from tkinter import messagebox
import pymysql.cursors
import random

# Connect to the SQL Server database
def connect_to_db():
    try:    
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="password",
            database="BankDB",  # Specify the database name if already created
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
        exit()

# Generate a 10-digit account number
def generate_account_number():
    return random.randint(1000000000, 9999999999)

# Create new account
def create_account(name, pin, city, contact):
    conn = connect_to_db()
    cursor = conn.cursor()
    account_number = generate_account_number()
    try:
        # Ensure PIN and contact are valid
        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("PIN must be exactly 4 digits!")
        if not contact.isdigit() or len(contact) != 10:
            raise ValueError("Contact number must be exactly 10 digits!")

        pin = int(pin)
        cursor.execute(
            "INSERT INTO BankAccount (AccountNumber, Name, Pin, City, Contact, Balance) VALUES (%s, %s, %s, %s, %s, %s)",
            (account_number, name, pin, city, contact, 0.0)
        )
        conn.commit()
        messagebox.showinfo("Success", f"Account created successfully!\nYour Account Number: {account_number}")
    except ValueError as ve:
        messagebox.showerror("Validation Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Could not create account: {e}")
    finally:
        conn.close()

# Authenticate existing user
def authenticate(account_number, pin):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM BankAccount WHERE AccountNumber = %s AND Pin = %s",
            (account_number, pin)
        )
        account = cursor.fetchone()
        return account
    except Exception as e:
        messagebox.showerror("Error", f"Authentication failed: {e}")
        return None
    finally:
        conn.close()

# GUI Functions
def welcome_screen():
    def handle_new_user():
        welcome_window.destroy()
        new_user_screen()

    def handle_existing_user():
        welcome_window.destroy()
        existing_user_screen()

    welcome_window = tk.Tk()
    welcome_window.title("Bank Management System")

    tk.Label(welcome_window, text="Welcome to the Bank", font=("Arial", 18)).pack(pady=10)

    tk.Button(welcome_window, text="New User", command=handle_new_user, width=20).pack(pady=5)
    tk.Button(welcome_window, text="Existing User", command=handle_existing_user, width=20).pack(pady=5)

    welcome_window.mainloop()

def new_user_screen():
    def submit():
        name = entry_name.get()
        pin = entry_pin.get()
        city = entry_city.get()
        contact = entry_contact.get()

        if not (name and pin and city and contact):
            messagebox.showerror("Error", "All fields are required!")
            return

        create_account(name, pin, city, contact)
        new_user_window.destroy()
        welcome_screen()

    new_user_window = tk.Tk()
    new_user_window.title("New User Registration")

    tk.Label(new_user_window, text="Name").pack()
    entry_name = tk.Entry(new_user_window)
    entry_name.pack()

    tk.Label(new_user_window, text="PIN (4 digits)").pack()
    entry_pin = tk.Entry(new_user_window, show="*")
    entry_pin.pack()

    tk.Label(new_user_window, text="City").pack()
    entry_city = tk.Entry(new_user_window)
    entry_city.pack()

    tk.Label(new_user_window, text="Contact (10 digits)").pack()
    entry_contact = tk.Entry(new_user_window)
    entry_contact.pack()

    tk.Button(new_user_window, text="Submit", command=submit).pack(pady=10)

    new_user_window.mainloop()

def existing_user_screen():
    def login():
        account_number = entry_account_number.get()
        pin = entry_pin.get()

        if not (account_number and pin):
            messagebox.showerror("Error", "All fields are required!")
            return

        account = authenticate(account_number, pin)
        if account:
            existing_user_window.destroy()
            account_screen(account)
        else:
            messagebox.showerror("Error", "Invalid account number or PIN!")

    existing_user_window = tk.Tk()
    existing_user_window.title("Existing User Login")

    tk.Label(existing_user_window, text="Account Number").pack()
    entry_account_number = tk.Entry(existing_user_window)
    entry_account_number.pack()

    tk.Label(existing_user_window, text="PIN").pack()
    entry_pin = tk.Entry(existing_user_window, show="*")
    entry_pin.pack()

    tk.Button(existing_user_window, text="Login", command=login).pack(pady=10)

    existing_user_window.mainloop()

def account_screen(account):
    def view_details():
        details = (
            f"Account Number: {account['AccountNumber']}\n"
            f"Name: {account['Name']}\n"
            f"City: {account['City']}\n"
            f"Contact: {account['Contact']}\n"
            f"Balance: {account['Balance']:.2f}"
        )
        messagebox.showinfo("Account Details", details)

    def credit():
        try:
            amount = float(entry_amount.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            
            conn = connect_to_db()
            cursor = conn.cursor()
            new_balance = account['Balance'] + amount
            cursor.execute(
                "UPDATE BankAccount SET Balance = %s WHERE AccountNumber = %s",
                (new_balance, account['AccountNumber'])
            )
            conn.commit()
            conn.close()
            
            account['Balance'] = new_balance  # Update the local account balance
            messagebox.showinfo("Success", f"Amount credited. New balance: {new_balance:.2f}")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Could not credit account: {e}")

    def debit():
        try:
            amount = float(entry_amount.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            if amount > account['Balance']:
                raise ValueError("Insufficient balance!")

            conn = connect_to_db()
            cursor = conn.cursor()
            new_balance = account['Balance'] - amount
            cursor.execute(
                "UPDATE BankAccount SET Balance = %s WHERE AccountNumber = %s",
                (new_balance, account['AccountNumber'])
            )
            conn.commit()
            conn.close()

            account['Balance'] = new_balance  # Update the local account balance
            messagebox.showinfo("Success", f"Amount debited. New balance: {new_balance:.2f}")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Could not debit account: {e}")

    account_window = tk.Tk()
    account_window.title("Account Options")

    tk.Label(account_window, text=f"Welcome, {account['Name']}", font=("Arial", 14)).pack()
    tk.Button(account_window, text="View Details", command=view_details).pack(pady=5)

    tk.Label(account_window, text="Enter Amount").pack()
    entry_amount = tk.Entry(account_window)
    entry_amount.pack()

    tk.Button(account_window, text="Credit", command=credit).pack(pady=5)
    tk.Button(account_window, text="Debit", command=debit).pack(pady=5)

    account_window.mainloop()


if __name__ == "__main__":
    welcome_screen()
