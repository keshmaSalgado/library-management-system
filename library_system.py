import csv
import os
from tabulate import tabulate
from datetime import datetime


MEMBER_HEADERS = ['id', 'firstName', 'lastName', 'contact', 'dateOfBirth', 'NationalId']
BOOK_HEADERS   = ['bookid', 'title', 'author', 'category', 'available']
BORROW_HEADERS = ['bookid', 'memberid', 'borrowdate', 'returndate']
USER_HEADERS  = ['username', 'password']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
memberfile = os.path.join(BASE_DIR, "members.csv")
booksfile = os.path.join(BASE_DIR, "books.csv")
borrowfile = os.path.join(BASE_DIR, "borrowdetailed.csv")
users_file = os.path.join(BASE_DIR, "users.csv")


# ---------- CSV Initialization ----------
def init_csv(file, headers):
    if not os.path.exists(file):
        with open(file, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
        print(f"File '{file}' created with headers.")
        
init_csv(memberfile, MEMBER_HEADERS)
init_csv(booksfile, BOOK_HEADERS)
init_csv(borrowfile, BORROW_HEADERS)
        
def init_users(file, headers):
    """Initialize users.csv with default admin account if not exists."""
    if not os.path.exists(file):
        with open(file, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            # Default admin user
            writer.writerow({"username": "admin1234", "password": "1234"})
        print(f"File '{file}' created with default admin user.")


init_users(users_file, USER_HEADERS)

    
# ---------- CSV Utility Functions ----------
def read_csv(file):
    with open(file, newline='') as f:
        return list(csv.DictReader(f))

def write_csv(file, data, fieldnames):
    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def append_csv(file, row):
    with open(file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)
        
# ---------- Member Functions ----------
def addMembers():
    # Read members once
    members = read_csv(memberfile)
    while True:
        try:
            memberID = int(input("Input the Id: "))
            if memberID <= 0:
                print("❌ Member ID must not be negative or zero.")
                continue
            if any(int(row["id"]) == memberID for row in members):
                print("❌ Member ID already exists.")
                continue
            break
        except ValueError:
            print("❌ Invalid input.Member ID must be a intiger")
    
    firstName = input('First Name: ')
    lastName = input('Last Name: ')
    contact = input('Contact: ')
    while True:
        dob_input = input("DOB (YYYY-MM-DD): ")
        try:
            dateOfBirth = datetime.strptime(dob_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
    nationalId = input('National ID: ')

    new_member = {
        "id": memberID,
        "firstName": firstName,
        "lastName": lastName,
        "contact": contact,
        "dateOfBirth": dateOfBirth.strftime("%Y-%m-%d"),  # always string
        "NationalId": nationalId
    }

    append_csv(memberfile, new_member)

    print(f"✅ Member {firstName} {lastName} added successfully!")

# ---------- Book Functions ----------
def addBooks():
    books = read_csv(booksfile)

    while True:
        try:
            bookID = int(input("Book Id: "))
            if bookID <= 0:
                print("❌ Must be positive.")
                continue
            if any(int(row["bookid"]) == bookID for row in books):
                print("❌ Book ID exists.")
                continue
            break
        except ValueError:
            print("❌ Invalid input.")
    
    title = input("Title: ")
    author = input("Author: ")
    category = input("Category: ").strip().lower()

    new_book = {
        "bookid": bookID,
        "title": title,
        "author": author,
        "category": category,
        "available": "True"
    }

    append_csv(booksfile, new_book)

    print(f"✅ Book '{title}' added successfully!")

# ---------- Borrow Functions ----------
def addBorrowedBooks():
    try:
        bookID = int(input('Book ID: '))
        memberID = int(input('Member ID: '))
    except ValueError:
        print("❌ Invalid input.")
        return
    while True:
        borrow_date_input = input("Borrow Date (YYYY-MM-DD): ")
        return_date_input = input("Return Date (YYYY-MM-DD): ")
        try:
            borrowDate = datetime.strptime(borrow_date_input, "%Y-%m-%d").date()
            returnDate = datetime.strptime(return_date_input, "%Y-%m-%d").date()
            if returnDate < borrowDate:
                print("❌ Return date cannot be before borrow date.")
                continue
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
    # Read members and books once
    members = read_csv(memberfile)
    books = read_csv(booksfile)

    if not any(int(row["id"]) == memberID for row in members):
        print("❌ Member not found.")
        return
    for book in books:
        if int(book["bookid"]) == bookID:
            if book["available"] != "True":
                print("❌ Book already borrowed.")
                return
            book["available"] = "False"
            break
    else:
        print("❌ Book ID not found.")
        return
    # Write back updated books
    write_csv(booksfile, books, BOOK_HEADERS)
    
    # Write borrow record
    borrow_record = {
        "bookid": bookID,
        "memberid": memberID,
        "borrowdate": borrowDate.strftime("%Y-%m-%d"),
        "returndate": returnDate.strftime("%Y-%m-%d")
    }
    append_csv(borrowfile, borrow_record)
    print("✅ Borrow record added.")
    
    
def returnBooks():
    try:
        bookID = int(input('Book ID to return: '))
    except ValueError:
        print("❌ Invalid input.")
        return

    borrowed = list(csv.DictReader(open(borrowfile)))
    books = list(csv.DictReader(open(booksfile)))
    found = False

    new_borrowed = []
    for record in borrowed:
        if int(record["bookid"]) == bookID:
            found = True
        else:
            new_borrowed.append(record)

    if not found:
        print("❌ Borrow record not found.")
        return

    # Update borrow CSV
    write_csv(borrowfile, new_borrowed, BORROW_HEADERS)

    # Mark book available
    for b in books:
        if int(b["bookid"]) == bookID:
            b["available"] = "True"
            break
    write_csv(booksfile, books, BOOK_HEADERS) 
 
    print("✅ Book returned.")

# ---------- Display Functions ----------

def getAllMembers():
    print("\n--- Members ---")
    members = read_csv(memberfile)
    if members:
        print(tabulate(members, headers="keys", tablefmt="grid"))
    else:
        print("No members found.")
        
def getAllBooks():
    print("\n--- Books ---")
    books = read_csv(booksfile)
    if books:
        print(tabulate(books, headers="keys", tablefmt="grid"))
    else:
        print("No books found.")
        
def getAllBorrowedDetailed():
    print("\n--- Borrowed ---")
    borrowed = read_csv(borrowfile)
    if borrowed:
        print(tabulate(borrowed, headers="keys", tablefmt="grid"))
    else:
        print("No borrowed records found.")
        
        
def getAllDetailed():
    getAllMembers()
    getAllBooks()
    getAllBorrowedDetailed()
    

# ---------- Search Functions ----------
def searchCSV(file, key, value):
    for row in read_csv(file):
        if str(row[key]) == str(value):
            print(tabulate([row.values()], headers=row.keys(), tablefmt="grid"))
            return
    print("❌ Not found.")

def searchMemberById():
    try:
        id_val = int(input("Member ID: "))
        searchCSV(memberfile, "id", id_val)
    except ValueError:
        print("❌ Invalid input.")

def searchBookByID():
    try:
        id_val = int(input("Book ID: "))
        searchCSV(booksfile, "bookid", id_val)
    except ValueError:
        print("❌ Invalid input.")

def searchBorrowDetailedById():
    try:
        id_val = int(input("Book ID: "))
        searchCSV(borrowfile, "bookid", id_val)
    except ValueError:
        print("❌ Invalid input.")

def searchBookByCategory():
    category_val = input("Enter category: ").strip().lower()
    books = read_csv(booksfile)
    found = False
    for b in books:
        if b["category"].lower() == category_val:
            print(f"Book ID:{b['bookid']} Title:{b['title']} Author:{b['author']} Available:{b['available']}")
            found = True
    if not found:
        print("❌ No books found in this category.")
        
def searchBookByAvailability():
    availability = input("Availability (True/False): ").strip().capitalize()
    if availability not in ["True", "False"]:
        print("❌ Invalid input. Use True or False.")
        return

    found = False
    for row in read_csv(booksfile):
        if row["available"] == availability:
            print(tabulate([row.values()], headers=row.keys(), tablefmt="grid"))
            found = True
    if not found:
        print("❌ No books found with availability =", availability)

        
# ----------- Update Functions (CSV-based) -----------
def updateMemberById():
    members = read_csv(memberfile)
    try:
        id_to_find = int(input('Enter the ID of the member to update: '))
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
        return

    updated = False
    for row in members:
        if int(row["id"]) == id_to_find:
            field = input('Enter the field to update (firstName, lastName, contact, dateOfBirth, NationalId): ').strip()
            if field not in row:
                print("❌ Invalid field.")
                return
            new_value = input(f'Enter new value for {field}: ').strip()
            if field == "dateOfBirth":
                try:
                    # Validate and format date
                    new_value = datetime.strptime(new_value, "%Y-%m-%d").date().strftime("%Y-%m-%d")
                except ValueError:
                    print("❌ Invalid date format. Use YYYY-MM-DD.")
                    return
            row[field] = new_value
            updated = True
            break

    if updated:
        write_csv(memberfile, members, MEMBER_HEADERS)
        print("✅ Member record updated successfully.")
    else:
        print("❌ Member not found.")

def updateBookById():
    books = read_csv(booksfile)  
    try:
        id_to_find = int(input('Enter the ID of the book to update: '))
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
        return
    updated = False
    for row in books:
        if int(row["bookid"]) == id_to_find:
            field = input('Enter the field to update (title, author, category, available): ').strip()
            if field not in row:
                print("❌ Invalid field.")
                return
            new_value = input(f'Enter new value for {field}: ').strip()
            
            # Handle category and availability consistently
            if field == "category":
                new_value = new_value.lower()
            elif field == "available":
                if new_value.lower() in ["true", "1", "yes"]:
                    new_value = "True"
                elif new_value.lower() in ["false", "0", "no"]:
                    new_value = "False"
                else:
                    print("❌ Invalid input for availability. Use True/False.")
                    return

            row[field] = new_value
            updated = True
            break

    if updated:
        with open(booksfile, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=BOOK_HEADERS)
            writer.writeheader()
            writer.writerows(books)
        print("✅ Book record updated successfully.")
    else:
        print("❌ Book not found.")
        
def updateBorrowedDetailedById():
    records = read_csv(borrowfile)  
    try:
        id_to_find = int(input('Enter the Book ID of the borrowed record to update: '))
    except ValueError:
        print("❌ Invalid Book ID.")
        return

    updated = False
    for row in records:
        if int(row["bookid"]) == id_to_find:
            field = input('Enter the field to update (bookid, memberid, borrowdate, returndate): ')
            if field not in row:
                print("❌ Invalid field.")
                return
            new_value = input(f"Enter new value for {field}: ").strip()
            if field in ["bookid", "memberid"]:
                try:
                    new_value = int(new_value)
                except ValueError:
                    print("❌ Must be a number.")
                    return
            elif field in ["borrowdate", "returndate"]:
                try:
                    new_value = datetime.strptime(new_value, "%Y-%m-%d").date().strftime("%Y-%m-%d")
                except ValueError:
                    print("❌ Invalid date format. Use YYYY-MM-DD.")
                    return
            row[field] = new_value
            updated = True
            break

    if updated:
        write_csv(borrowfile, records, BORROW_HEADERS)
        print("✅ Borrowed record updated successfully.")
    else:
        print("❌ Borrowed record not found.")

# ----------- Remove Functions (CSV-based) -----------
def remove_member_by_id():
    reader= read_csv(memberfile)  
    try:
        member_id = int(input('Input the ID of the member to remove: '))
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
        return

    removed = False
    new_rows = [row for row in reader if int(row["id"]) != member_id]
    if len(new_rows) < len(reader):
        removed = True

    if removed:
        write_csv(memberfile, new_rows,MEMBER_HEADERS)
        print(f"✅ Member with ID {member_id} has been removed.")
    else:
        print("❌ Member not found.")


def remove_book_by_id():
    books = read_csv(booksfile)  
    try:
        book_id = int(input('Input the ID of the book to remove: '))
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
        return

    new_rows = [row for row in books if int(row["bookid"]) != book_id]
    if len(new_rows) < len(books):
        write_csv(booksfile, new_rows, BOOK_HEADERS)  
        print(f"✅ Book with ID {book_id} has been removed.")
    else:
        print("❌ Book not found.")



def remove_borrowdetailed_by_id():
    record = read_csv(borrowfile) 
    try:
        borrow_id = int(input('Input the Book ID of the borrow record to remove: '))
    except ValueError:
        print("❌ Invalid Book ID. Please enter a number.")
        return

    removed = False

    new_rows = [row for row in record if int(row["bookid"]) != borrow_id]
    if len(new_rows) < len(record):
        write_csv(borrowfile, new_rows, BORROW_HEADERS)  
        print(f"✅ Borrowed record with Book ID {borrow_id} has been removed.")
    else:
        print("❌ Borrowed record not found.")

        
def helpMenu():
    print("""
    =============================
    📚 Library Management System
    =============================
    - Use option 1 to add members, books, or borrow/return records.
    - Use option 2 to display members, books, or borrow/return details.
    - Use option 3 to search records by ID.
    - Use option 4 to update records.
    - Use option 5 to delete records.
    - Use option 6 to log out and exit.
    """)
    
    
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_and_clear():
    input("\n🔹 Press Enter/Space to continue...")
    clear_console()


# ------------ Main Menu ------------
def main():
    while True:
        pause_and_clear()

        helpMenu()
        
        try:
            choice = int(input('Enter your choice (1-6): '))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if choice == 1:
            while True:
                print("    1. Add Members")
                print("    2. Add Books")
                print("    3. Add Borrowed Books")
                print("    4. Return Books")
                print("    5. go to back to help menu")
                try:
                    submenu_choice = int(input('Enter your choice (1-5): '))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                if submenu_choice == 1:
                    addMembers()
                elif submenu_choice == 2:
                    addBooks()
                elif submenu_choice == 3:
                    addBorrowedBooks()
                elif submenu_choice == 4:
                    returnBooks()
                elif submenu_choice == 5:
                    break
                else:
                    print("❌ Invalid choice.")
                
                
        elif choice == 2:
            while True:
                print("    1. Display All Members")
                print("    2. Display All Books")
                print("    3. Display All Borrowed Detailed")
                print("    4. Display All Details")
                print("    5. go to back to help menu")
                try:
                    submenu_choice = int(input('Enter your choice (1-5): '))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                if submenu_choice == 1:
                    getAllMembers()
                elif submenu_choice == 2:
                    getAllBooks()
                elif submenu_choice == 3:
                    getAllBorrowedDetailed()
                elif submenu_choice == 4:
                    getAllDetailed()
                elif submenu_choice == 5:
                    break
                else:
                    print("❌ Invalid choice.")           
        elif choice == 3:
            while True:                
                print("    1. Search member by ID")
                print("    2. Search Books by ID")
                print("    3. Search Books by Category")
                print("    4. Search BorrowedDetailed by Book ID")
                print("    5. Search Book by Availability")
                print("    6. go to back to help menu")
                try:
                    submenu_choice = int(input('Enter your choice (1-6): '))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                if submenu_choice == 1:
                    searchMemberById()
                elif submenu_choice == 2:
                    searchBookByID()
                elif submenu_choice == 3:
                    searchBookByCategory()                    
                elif submenu_choice == 4:
                    searchBorrowDetailedById()
                elif submenu_choice == 5:
                    searchBookByAvailability()                    
                elif submenu_choice == 6:
                    break
                else:
                    print("❌ Invalid choice.")
                    
                
        elif choice == 4:
            while True:
                print("    1. Update member by ID")
                print("    2. Update Books by ID")
                print("    3. Update BorrowedDetailed by ID")
                print("    4. go to back to help menu")
                try:
                    submenu_choice = int(input('Enter your choice (1-4): '))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                if submenu_choice == 1:
                    updateMemberById()
                elif submenu_choice == 2:
                    updateBookById()
                elif submenu_choice == 3:
                    updateBorrowedDetailedById()
                elif submenu_choice == 4:
                    break
                else:
                    print("❌ Invalid choice.")
            
        elif choice == 5:
            while True:
                print("    1. Delete member")
                print("    2. Delete Books")
                print("    3. Delete BorrowedDetailed")
                print("    4. go to back to help menu")
                try:
                    submenu_choice = int(input('Enter your choice (1-4): '))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                if submenu_choice == 1:
                    remove_member_by_id()
                elif submenu_choice == 2:
                    remove_book_by_id()
                elif submenu_choice == 3:
                    remove_borrowdetailed_by_id()
                elif submenu_choice == 4:
                    break
                else:
                    print("❌ Invalid choice.")
                    
        elif choice == 6:
            print("Good Bye 👋Exiting...")
            pause_and_clear() 
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")



def member_login():
    """Allow library members to log in using ID and first name."""
    while True:
        clear_console()
        print("================================")
        print("   📚 Library Management System ")
        print("         Member Access")
        print("================================")
        
        
        try:
            member_id = int(input("Enter your Member ID: ").strip())
        except ValueError:
            print("❌ Member ID must be a number.")
            input("Press Enter to try again...")
            continue

        first_name = input("Enter your First Name: ").strip()

        members = read_csv(memberfile)
        for member in members:
            if int(member["id"]) == member_id and member["firstName"].lower() == first_name.lower():
                print(f"👍 Welcome {member['firstName']}!")
                input("Press Enter to continue...")
                return member  # Return the member dict for reference

        print("❌ Member not found. Please check your ID and first name.")
        choice = input("Do you want to try again? (y/n): ").strip().lower()
        if choice == "n":  # 👈 Go back to main login
            print("⬅️ Returning to main login menu...")
            input("Press Enter to continue...")
            return None
        
    
            
def admin_login():
    """Allow admin users to log in using username and password."""
    while True:
        print("================================")
        print("   📚 Library Management System ")
        print("            Login Page")
        print("================================")
        enterName = input("🙍 Enter username: ").strip()
        enterPassword = input("🔒 Enter password: ").strip()
        
        # Read users from CSV
        with open(users_file, newline='') as f:
            users = list(csv.DictReader(f))
        
        # Match credentials
        for user in users:
            if user["username"] == enterName and user["password"] == enterPassword:
                print("👍 Login successful.")
                pause_and_clear()
                main()  # 🚀 Your main menu
                return True
        
        print("❌ Username or password is incorrect")
        pause_and_clear()   

def member_menu(member):
    """Menu for logged-in members to search books."""
    while True:
        clear_console()
        print('========================================================================')
        print(f"📚 Library System - Member: {member['firstName']} (ID: {member['id']})")
        print('========================================================================')
        print("1. Search book by ID")
        print("2. Search book by Category")
        print("3. Search book by Availability")
        print("4. Back to main login menu")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            searchBookByID()
            input("Press Enter to continue...")
        elif choice == "2":
            searchBookByCategory()
            input("Press Enter to continue...")
        elif choice == "3":
            searchBookByAvailability()
            input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            
def login():
    while True:
        clear_console()
        print("================================")
        print("   📚 Library Management System ")
        print("            Login Page")
        print("================================")
        print("1. Admin login")
        print("2. Member login (basic access)")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            admin_login()  # Your existing admin login logic
        elif choice == "2":
            member = member_login()
            if member:
                member_menu(member)
        elif choice == "3":
            print("Good Bye 👋Exiting...")
            break
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            
login()



    

    
    
    

