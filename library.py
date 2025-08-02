import json
import os

BOOKS_FILE = "books.json"
BORROW_FILE = "borrowed.json"

# Load or create files
def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# View all books
def view_books():
    books = load_data(BOOKS_FILE)
    if not books:
        print("No books available.\n")
    else:
        print("\n--- Available Books ---")
        for book in books:
            print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")
        print()

# Admin: Add book
def add_book():
    books = load_data(BOOKS_FILE)
    book_id = input("Enter book ID: ")
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    quantity = int(input("Enter quantity: "))

    books.append({
        "id": book_id,
        "title": title,
        "author": author,
        "quantity": quantity
    })
    save_data(BOOKS_FILE, books)
    print("✅ Book added successfully.\n")

# Admin: Remove book
def remove_book():
    books = load_data(BOOKS_FILE)
    book_id = input("Enter book ID to remove: ")
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_data(BOOKS_FILE, books)
            print("✅ Book removed.\n")
            return
    print("❌ Book not found.\n")

# User: Borrow book
def borrow_book():
    books = load_data(BOOKS_FILE)
    borrowed = load_data(BORROW_FILE)
    user = input("Enter your name: ")
    book_id = input("Enter book ID to borrow: ")

    for book in books:
        if book["id"] == book_id:
            if book["quantity"] > 0:
                book["quantity"] -= 1
                borrowed.append({"user": user, "book_id": book_id, "title": book["title"]})
                save_data(BOOKS_FILE, books)
                save_data(BORROW_FILE, borrowed)
                print("✅ Book borrowed.\n")
                return
            else:
                print("⛔ Book out of stock.\n")
                return
    print("❌ Book not found.\n")

# User: Return book
def return_book():
    borrowed = load_data(BORROW_FILE)
    books = load_data(BOOKS_FILE)
    user = input("Enter your name: ")
    book_id = input("Enter book ID to return: ")

    for entry in borrowed:
        if entry["user"] == user and entry["book_id"] == book_id:
            borrowed.remove(entry)
            for book in books:
                if book["id"] == book_id:
                    book["quantity"] += 1
                    save_data(BOOKS_FILE, books)
                    save_data(BORROW_FILE, borrowed)
                    print("✅ Book returned.\n")
                    return
    print("❌ No such borrowed book found.\n")

# User: View borrowed books
def view_borrowed():
    borrowed = load_data(BORROW_FILE)
    user = input("Enter your name: ")
    found = False
    print("\n--- Your Borrowed Books ---")
    for entry in borrowed:
        if entry["user"] == user:
            print(f"Book ID: {entry['book_id']}, Title: {entry['title']}")
            found = True
    if not found:
        print("No borrowed books found.")
    print()

# Menu
def main():
    while True:
        print("====== Library Management System ======")
        print("1. View Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. View My Borrowed Books")
        print("5. Admin - Add Book")
        print("6. Admin - Remove Book")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_books()
        elif choice == "2":
            borrow_book()
        elif choice == "3":
            return_book()
        elif choice == "4":
            view_borrowed()
        elif choice == "5":
            add_book()
        elif choice == "6":
            remove_book()
        elif choice == "7":
            print("🙏 Thank you for using Library System.")
            break
        else:
            print("⚠️ Invalid choice.\n")

if __name__ == "__main__":
    main()
