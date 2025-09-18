📚 City Library Management System (Python + CSV File Handling)
📚 City Library Management System (Python + CSV File Handling)

This project is a menu-driven Library Management System built entirely in Python using CSV file handling for data storage.
It allows administrators to manage library books, members, and borrow records, and allows members to search books with basic access.

🚀 How to Run

1.Install Python
Make sure Python 3.8+ is installed on your computer.
Verify by running:

python --version


or

python3 --version


2.Install Required Library
The program uses tabulate to display data in a table format.
Install it with:

pip install tabulate


Run the Program
Open a terminal/command prompt in the project folder and run:

python library_system.py


(Replace library_system.py with your file name if it's different.)

First Run Setup
On the first run, the program will automatically create:

members.csv

books.csv

borrowdetailed.csv

users.csv (with default admin account admin1234 / 1234)

📋 Features
🔑 Admin Features

Add members, books, and borrow records

View all members, books, borrow records

Search for members, books (by ID, category, availability), borrow records

Update members, books, and borrow records

Delete members, books, borrow records

Return Books updates availability automatically

👥 Member Features

Login using Member ID and First Name

Search books by:

Book ID

Category

Availability

🎯 Additional Features

CSV-based file storage (no external database needed)

Menu-driven navigation for better user experience

Input validation (numeric checks, duplicate ID prevention, date validation)

Ability to go back to the main login menu after failed member login attempts

📦 Dependencies

Python: Version 3.8 or higher

Built-in Libraries:

csv

os

datetime

External Library:

tabulate
 → install using pip install tabulate

🧪 Example Admin Login
Username: admin1234
Password: 1234


Once logged in, you will be presented with the main menu options.

⚠️ Known Limitations / Future Improvements

No password change feature (admin password must be manually changed in users.csv)

No multiple admin accounts support

No overdue book reminder (could be added as enhancement)

No transaction history or fine calculation for late returns

Console-based only (no GUI)

📂 File Structure
project-folder/
│
├── library_system.py        # Main program file
├── members.csv              # Auto-created on first run
├── books.csv                # Auto-created on first run
├── borrowdetailed.csv       # Auto-created on first run
└── users.csv                # Auto-created with default admin credentials