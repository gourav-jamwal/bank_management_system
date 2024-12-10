🏦 Bank Management System
A simple and interactive GUI-based Bank Management System developed using Python's Tkinter for the frontend and MySQL for the backend. This system allows users to manage their bank accounts with features like account creation, login, credit, debit, and viewing account details.

✨ Features
New User Registration: Users can create a new bank account with a unique 10-digit account number.
Secure Login: Users log in using their account number and 4-digit PIN.
Balance Management:
Credit Money: Add funds to the account.
Debit Money: Withdraw funds (with balance checks).
Account Details: View account holder's details including current balance.
Realistic Validation:
PIN must be exactly 4 digits.
Contact number must be exactly 10 digits.
Prevent overdrafts during debits.

🖥️ Technologies Used
Programming Language: Python
Database: MySQL
GUI Library: Tkinter
Additional Modules:
pymysql for database connectivity.
random for generating unique account numbers.

🚀 Getting Started
Follow the steps below to set up and run the project on your system.

Prerequisites
Python: Make sure Python 3.8 or above is installed on your system.
MySQL: Install MySQL Server and create a database named BankDB.
Dependencies: Install required Python libraries:
bash
Copy code
pip install pymysql

Database Setup
Open your MySQL client and run the following commands to create the BankAccount table:

sql
Copy code
CREATE DATABASE BankDB;

USE BankDB;

CREATE TABLE BankAccount (
    AccountNumber BIGINT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Pin INT NOT NULL,
    City VARCHAR(100),
    Contact VARCHAR(10),
    Balance DECIMAL(10, 2) DEFAULT 0.00
);

Running the Application
Clone or download this repository to your local machine.

Open a terminal in the project directory and run:
bash
Copy code
python app.py
The application will launch with a GUI window. Start managing your bank accounts! 🎉


🤝 Contributing
Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and submit a pull request.