import csv
import os
from tabulate import tabulate

members = []
books = []
borrowDetailed = []
memberfile = "members.csv"
booksfile = "books.csv"
borrowfile = "borrowdetailed.csv"

# Load members
if os.path.exists(memberfile):
    with open(memberfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            member = {
                "id": int(row["id"]),
                "firstName": row["firstName"],
                "lastName": row["lastName"],
                "contact": row["contact"],
                "dateOfBirth": row["dateOfBirth"],
                "NationalId": row["NationalId"]
            }
            members.append(member)  # ✅ fixed
else:
    with open(memberfile, mode='w', newline='') as csvfile:
        fieldnames = ['id', 'firstName', 'lastName', 'contact', 'dateOfBirth', 'NationalId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    print(f"File '{memberfile}' created with headers.")

# Load books
if os.path.exists(booksfile):
    with open(booksfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            book = {
                "bookid": int(row["bookid"]),
                "title": row["title"],
                "author": row["author"],
                "category": row["category"],
                "available": row["available"],
            }
            books.append(book)  # ✅ fixed
else:
    with open(booksfile, mode='w', newline='') as csvfile:
        fieldnames = ['bookid', 'title', 'author', 'category', 'available']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    print(f"File '{booksfile}' created with headers.")

# Load borrow records
if os.path.exists(borrowfile):
    with open(borrowfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            borrow = {
                "bookid": int(row["bookid"]),
                "memberid": int(row["memberid"]),
                "borrowdate": row["borrowdate"],
                "returndate": row["returndate"]
            }
            borrowDetailed.append(borrow)
else:
    with open(borrowfile, mode='w', newline='') as csvfile:
        fieldnames = ['bookid', 'memberid', 'borrowdate', 'returndate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    print(f"File '{borrowfile}' created with headers.")


# ------------ Member Management Functions ------------
#--------Add Detailed
def addMembers():
    while True:
        try:
            memberID = int(input("Input the Id: "))
            if memberID <= 0:
                print("❌ Member ID must be a positive number.")
                continue
            # --- Check for duplicate ID ---
            for member in members:
                if member["id"] == memberID:
                    print("❌ Member ID already exists. Please enter a different ID.")
                    break
            else:  # runs only if no duplicate found
                break
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    firstName = input('Input the First Name: ')
    lastName = input('Input the Last Name: ')
    contact = input('Input the Contact: ')
    dateOfBirth = input('Input the Date of Birth (YYYY-MM-DD): ')
    nationalId = input('Input the National Id: ')

    members.append({
        "id": memberID,
        "firstName": firstName,
        "lastName": lastName,
        "contact": contact,
        "dateOfBirth": dateOfBirth,
        "NationalId": nationalId
    })
    
def addBooks():
    while True:
        try:
            bookID = int(input("Input the Book Id: "))
            if bookID <= 0:
                print("❌ Book ID must be a positive number.")
                continue
            # --- Check if Book ID already exists ---
            for book in books:
                if book["bookid"] == bookID:
                    print("❌ Book ID already exists. Please enter a different ID.")
                    break
            else:  # only runs if no duplicate found
                break
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    title = input('Input the Book Title: ')
    author = input('Input the Author: ')
    category = input('Input the Category: ')
    books.append({
        "bookid": bookID,
        "title": title,
        "author": author,
        "category": category,
        "available": True
    })

def addBorrowedBooks():
    bookID = int(input('Input the Book Id: '))
    memberID = int(input('Input the Member Id: '))
    borrowDate = input('Input the Borrow Date (YYYY-MM-DD): ')
    returnDate = input('Input the Return Date (YYYY-MM-DD): ')

    # Check if book exists
    for book in books:
        if book["bookid"] == bookID:
            if not book["available"]:
                print("❌ This book is already borrowed.")
                return
            # Mark as borrowed
            book["available"] = False
            borrowDetailed.append({
                "bookid": bookID,
                "memberid": memberID,
                "borrowdate": borrowDate,
                "returndate": returnDate
            })
            print("✅ Borrow record added. Book marked unavailable.")
            return

    print("❌ Book ID not found.")
    
def returnBooks():
    bookID = int(input('Input the Book Id: '))

    # Find borrow record
    borrow_found = None
    for borrow in borrowDetailed:
        if borrow["bookid"] == bookID:
            borrow_found = borrow
            break

    if borrow_found is None:
        print("❌ No borrow record found for this Book ID.")
        return False

    # Find the book and mark available
    for book in books:
        if book["bookid"] == bookID:
            book["available"] = True  # ✅ always set to available when returning
            break

    # Remove borrow record
    borrowDetailed.remove(borrow_found)
    print(f"✅ Book ID {bookID} has been returned. Borrow record removed, book marked available.")
    return True


# ------------ Display Functions ------------
def getAllDetailed():
    print("\n\nMembers Detailed")
    if not members:
        print("No members found.")
    else:
        member_table = [[m["id"], m["firstName"], m["lastName"], m["contact"], m["dateOfBirth"], m["NationalId"]] for m in members]
        print(tabulate(member_table, headers=["ID", "First Name", "Last Name", "Contact", "DOB", "National ID"], tablefmt="grid"))

    print("\n\nBooks")
    if not books:
        print("No Books found.")
    else:
        book_table = [[b["bookid"], b["title"], b["author"], b["category"], b["available"]] for b in books]
        print(tabulate(book_table, headers=["Book ID", "Title", "Author", "Category", "Available"], tablefmt="grid"))

    print("\n\nBorrowed Detailed")
    if not borrowDetailed:
        print("No Borrowed Records found.")
    else:
        borrow_table = [[bd["bookid"], bd["memberid"], bd["borrowdate"], bd["returndate"]] for bd in borrowDetailed]
        print(tabulate(borrow_table, headers=["Book ID", "Member ID", "Borrow Date", "Return Date"], tablefmt="grid"))


#--------Search Detailed
def searchMemberById():
    member_id = int(input('Input the id: '))
    for member in members:
        if member["id"] == member_id:
            print(f"id:{member['id']} First Name:{member['firstName']} Last Name:{member['lastName']} Contact:{member['contact']} DOB:{member['dateOfBirth']} NationalId:{member['NationalId']}")
            return
    print("No member found!!!!")

def searchBookByID():
    book_id = int(input('Input the id: '))
    for book in books:
        if book["bookid"] == book_id:
            print(f"id:{book['bookid']} title:{book['title']} author:{book['author']} category:{book['category']} available:{book['available']}")
            return
    print("No book found!!!!")

def searchBorrowDetailedById():
    borrow_id = int(input('Input the id: '))
    for borrow in borrowDetailed:
        if borrow["bookid"] == borrow_id:
            print(f"Book ID:{borrow['bookid']} Member ID:{borrow['memberid']} Borrow Date:{borrow['borrowdate']} Return Date:{borrow['returndate']}")
            return
    print("No borrow record found!!!!")

#--------Update Detailed
def updateMemberById():
    id_to_find = int(input('Enter the id of the member to update: '))
    for member in members:
        if member["id"] == id_to_find:
            field = input('Enter the field to update (name, age, NationalId): ')
            if field in member:
                new_value = input(f'Enter new value for {field}: ')
                if field == "age":
                    new_value = int(new_value)
                member[field] = new_value
                print("Member record updated successfully.")
                return True
            else:
                print("Invalid field.")
                return False
    print("Member not found.")
    return False

def updateBookById():
    id_to_find = int(input('Enter the id of the book to update: '))
    for book in books:
        if book["bookid"] == id_to_find:
            field = input('Enter the field to update (name, available): ')
            if field in book:
                new_value = input(f'Enter new value for {field}: ')
                if field == "available":
                    new_value = int(new_value)
                book[field] = new_value
                print("Book record updated successfully.")
                return True
            else:
                print("Invalid field.")
                return False
    print("Book not found.")
    return False

def updateBorrowedDetailedById():
    id_to_find = int(input('Enter the id of the borrowed record to update: '))
    for borrow in borrowDetailed:
        if borrow["bookid"] == id_to_find:
            field = input('Enter the field to update (bookid, memberid, borrowdate, returndate): ')
            if field in borrow:
                new_value = input(f'Enter new value for {field}: ')
                if field == "bookid":
                    new_value = int(new_value)
                borrow[field] = new_value
                print("Borrow record updated successfully.")
                return True
            else:
                print("Invalid field.")
                return False
    print("Member not found.")
    return False

#--------Remove Detailed
def remove_member_by_id():
    member_id = int(input('Input the id: '))
    for i, member in enumerate(members):
        if member["id"] == member_id:
            del members[i]
            print(f"Member with ID {member_id} has been removed.")
            return True
    print("Member not found.")
    return False

def remove_member_by_id():
    member_id = int(input('Input the id: '))
    for i, member in enumerate(members):
        if member["id"] == member_id:
            del members[i]
            print(f"Member with ID {member_id} has been removed.")
            return True
    print("Member not found.")
    return False



def remove_book_by_id():
    book_id = int(input('Input the id: '))
    for i, book in enumerate(books):
        if book["bookid"] == book_id:
            del books[i]
            print(f"Book with ID {book_id} has been removed.")
            return True
    print("Book not found.")
    return False

def remove_borrowdetailed_by_id():
    borrow_id = int(input('Input the id: '))
    for i, borrow in enumerate(borrowDetailed):
        if borrow["bookid"] == borrow_id:
            del borrowDetailed[i]
            print(f"Borrow record with ID {borrow_id} has been removed.")
            return True
    print("Borrow record not found.")
    return False

#--------Save Detailed
def save_members_to_csv(memberfile="members.csv"):
    with open(memberfile, 'w', newline='') as csvfile:
        fieldnames = ['id', 'firstName', 'lastName', 'contact', 'dateOfBirth', 'NationalId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for member in members:
            writer.writerow(member)
            
def save_books_to_csv(bookfile="books.csv"):
    with open(bookfile, 'w', newline='') as csvfile:
        fieldnames = ['bookid', 'title', 'author', 'category', 'available']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

def save_borrowdetailed_to_csv(borrowfile="borrowdetailed.csv"):
    with open(borrowfile, 'w', newline='') as csvfile:
        fieldnames = ['bookid', 'memberid', 'borrowdate', 'returndate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for borrow in borrowDetailed:
            writer.writerow(borrow)

# ------------ Main Menu ------------
def main():
    while True:
        print("\n--- Member Management Menu ---")
        print("1. Add member/books/borrowed detailed/Returned book")
        print("2. Get all details")
        print("3. Search member/books/borrowed detailed by ID")
        print("4. Update member/books/borrowed detailed")
        print("5. Delete member/books/borrowed detailed")
        print("6. Save and Exit")

        try:
            choice = int(input('Enter your choice (1-6): '))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if choice == 1:
            print("1. Add member")
            print("2. Add Books")
            print("3. Add BorrowedDetailed")
            print("4. Add Return book")
            try:
                choice = int(input('Enter your choice (1-4): '))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if choice == 1:
                addMembers()
            elif choice == 2:
                addBooks()
            elif choice == 3:
                addBorrowedBooks()
            elif choice == 4:
                returnBooks()
            else:
                print("❌ Invalid choice.")         
        elif choice == 2:
            getAllDetailed()
        elif choice == 3:
            print("1. Search member")
            print("2. Search Books")
            print("3. Search BorrowedDetailed")
            try:
                choice = int(input('Enter your choice (1-3): '))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if choice == 1:
                searchMemberById()
            elif choice == 2:
                searchBookByID()
            elif choice == 3:
                searchBorrowDetailedById()
            else:
                print("❌ Invalid choice.")
        elif choice == 4:
            print("1. Update member")
            print("2. Update Books")
            print("3. Update BorrowedDetailed")
            try:
                choice = int(input('Enter your choice (1-3): '))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if choice == 1:
                updateMemberById()
            elif choice == 2:
                updateBookById()
            elif choice == 3:
                updateBorrowedDetailedById()
            else:
                print("❌ Invalid choice.")
        elif choice == 5:
            print("1. Delete member")
            print("2. Delete Books")
            print("3. Delete BorrowedDetailed")
            try:
                choice = int(input('Enter your choice (1-3): '))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if choice == 1:
                remove_member_by_id()
            elif choice == 2:
                remove_book_by_id()
            elif choice == 3:
                remove_borrowdetailed_by_id()
            else:
                print("❌ Invalid choice.")
        elif choice == 6:
            save_members_to_csv()
            save_books_to_csv()
            save_borrowdetailed_to_csv()
            print("Thank you! Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


username = 'admin1234'
password = "1234"


# while True:
#     enterName = input("Enter username: ")
#     enterPassword = input("Enter password: ")

#     if enterName == username and enterPassword == password:
        
#         break
#     else:
#         print("Username or password is incorrect")

        
main()
    

    
    
    

