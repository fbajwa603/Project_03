import unittest
from datetime import date

from libraryItem import AbstractLibraryItem, LibraryItem, Book, Journal, DVD, EBook
from User import User
from library_system import LibrarySystem


class TestInheritanceAndABC(unittest.TestCase):
    def test_abstract_library_item_is_abstract(self):
        with self.assertRaises(TypeError):
            AbstractLibraryItem()  

    def test_subclasses_are_instances(self):
        b = Book("B1", "Title", ["author"], set(), 1)
        self.assertIsInstance(b, LibraryItem)
        self.assertIsInstance(b, AbstractLibraryItem)


class TestPolymorphism(unittest.TestCase):
    def setUp(self):
        self.student_role = "Student"
        self.faculty_role = "Faculty"
        self.checkout = date(2025, 3, 1)

        self.book = Book("BK", "Book", ["a"], set(), 1)
        self.journal = Journal("JR", "Journal", ["a"], set(), 1)
        self.dvd = DVD("DV", "DVD", ["a"], set(), 1)
        self.ebook = EBook("EB", "EBook", ["a"], set(), 1)

    def test_different_due_dates_for_student(self):
        b_due = self.book.calculate_due_date(self.checkout, self.student_role)
        j_due = self.journal.calculate_due_date(self.checkout, self.student_role)
        d_due = self.dvd.calculate_due_date(self.checkout, self.student_role)
        e_due = self.ebook.calculate_due_date(self.checkout, self.student_role)

        self.assertEqual((b_due - self.checkout).days, 14)
        self.assertEqual((j_due - self.checkout).days, 7)
        self.assertEqual((d_due - self.checkout).days, 7)
        self.assertEqual(e_due, self.checkout)

    def test_get_item_type_polymorphism(self):
        items = [self.book, self.journal, self.dvd, self.ebook]
        types_seen = {i.get_item_type() for i in items}
        self.assertEqual(types_seen, {"Book", "Journal", "DVD", "EBook"})


class TestComposition(unittest.TestCase):
    def test_library_system_composition_checkout(self):
        system = LibrarySystem("Test Library")
        user = User("U1", "jane doe", "Student")
        system.add_user(user)

        book = Book("B1", "Test Book", ["a"], set(), 1)
        system.add_item(book)

        loan = system.checkout_item("L1", user.user_id, book.item_id, date(2025, 3, 1))
        self.assertEqual(loan.item_id, book.item_id)
        self.assertEqual(loan.user_id, user.user_id)
        self.assertEqual(user.get_active_loan_count(), 1)


if __name__ == "__main__":
    unittest.main()
