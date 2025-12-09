from datetime import date

from User import User
from libraryItem import LibraryItem, Book, Journal, DVD, EBook
from catalog import Catalog
from loan import Loan
from Hold import Hold
from library_system import LibrarySystem


print("\n=== CREATE USER ===")
u = User("U001", "john doe", "Student")
print(u)

print("\n=== CREATE ITEM ===")
i = LibraryItem("B001", "Python Book", ["guido"], {"programming"}, 3)
print(i)

print("\n=== CREATE CATALOG AND ADD ITEM ===")
c = Catalog("Main Library")
c.add_item(i)
print(c)

print("\n=== SEARCH CATALOG ===")
c.search_by_keyword("python")

print("\n=== CHECK OUT A COPY ===")
i.checkout_copy()
print("Available copies after checkout:", i.available_copies)

print("\n=== CREATE LOAN ===")
checkout = date(2025, 1, 1)
due = u.calculate_due_date(checkout)
loan = Loan("L001", u.user_id, i.item_id, due)
print(loan)

print("\n=== RETURN ITEM LATE ===")
fine = loan.return_item(i, date(2025, 1, 20))
print("Fine:", fine)

print("\n=== CREATE HOLD ===")
h = Hold("H001", u.user_id, i.item_id, date(2025, 1, 1), date(2025, 1, 10))
print(h)
print("Hold active on Jan 5:", h.is_active(date(2025, 1, 5)))
print("Hold expired by Jan 15:", h.is_expired(date(2025, 1, 15)))

print("\n=== SECOND SCENARIO: FACULTY USER ===")
f = User("U010", "professor smith", "Faculty")
print("\n=== CREATE FACULTY USER ===")
print(f)

i2 = LibraryItem("B010", "Advanced algorithms", ["robertson"], {"cs", "algorithms"}, 2)
print("\n=== CREATE SECOND ITEM ===")
print(i2)

print("\n=== ADD SECOND ITEM TO CATALOG ===")
c.add_item(i2)
print(c)

print("\n=== FACULTY SEARCH ===")
c.search_by_keyword("algorithms")

print("\n=== FACULTY CHECKOUT ===")
i2.checkout_copy()
print("Available copies after checkout:", i2.available_copies)

print("\n=== CREATE FACULTY LOAN ===")
checkout_f = date(2025, 2, 1)
due_f = f.calculate_due_date(checkout_f)
loan_f = Loan("L010", f.user_id, i2.item_id, due_f)
print(loan_f)

print("\n=== FACULTY RETURNS LATE ===")
fine_f = loan_f.return_item(i2, date(2025, 2, 25))
print("Faculty Fine:", fine_f)

print("\n=== FACULTY HOLD ===")
hf = Hold("H010", f.user_id, i2.item_id, date(2025, 2, 1), date(2025, 2, 20))
print(hf)
print("Faculty hold active Feb 10:", hf.is_active(date(2025, 2, 10)))
print("Faculty hold expired Feb 25:", hf.is_expired(date(2025, 2, 25)))


print("\n=== PROJECT 3: INHERITANCE & POLYMORPHISM DEMO ===")

system = LibrarySystem("Project 3 Library")

student = User("U100", "alice student", "Student")
faculty = User("U200", "bob faculty", "Faculty")
system.add_user(student)
system.add_user(faculty)

book = Book("BK001", "Intro to Databases", ["kim"], {"cs", "database"}, 3,
            genre="Textbook")
journal = Journal("JR001", "Journal of Data Science", ["lee"], {"data"}, 2)
dvd = DVD("DV001", "Science Documentary", ["doe"], {"video", "science"}, 1)
ebook = EBook("EB001", "Python E-Book", ["guido"], {"programming", "ebook"}, 999)

# Composition: LibrarySystem has-a Catalog that stores items
for item in [book, journal, dvd, ebook]:
    system.add_item(item)

items = [book, journal, dvd, ebook]
checkout_date = date(2025, 3, 1)

print("\n-- Polymorphic due dates for STUDENT --")
for item in items:
    due_date = item.calculate_due_date(checkout_date, student.role)
    print(f"{item.get_item_type():7} '{item.title}' due on {due_date.isoformat()}")

print("\n-- Polymorphic due dates for FACULTY --")
for item in items:
    due_date = item.calculate_due_date(checkout_date, faculty.role)
    print(f"{item.get_item_type():7} '{item.title}' due on {due_date.isoformat()}")

print("\n-- LibrarySystem composition checkout demo --")
loan_b = system.checkout_item("L100", student.user_id, book.item_id, checkout_date)
print("Created loan via LibrarySystem:", loan_b)

loan_d = system.checkout_item("L101", faculty.user_id, dvd.item_id, checkout_date)
print("Created loan via LibrarySystem:", loan_d)
