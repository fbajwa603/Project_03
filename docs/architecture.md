# Project 3 – Architecture Overview

## 1. Purpose
This project extends the Library Management System from Project 2 by adding:

- Inheritance
- Abstract Base Classes (ABC)
- Polymorphism
- Composition
- A coordinating class called LibrarySystem

The goal is to enhance the original system with advanced OOP design.

---

## 2. Inheritance Hierarchy

The inheritance structure focuses on library items.

```
AbstractLibraryItem (ABC)
        |
        v
   LibraryItem
        |
   ---------------------------------------
   |        |         |                 |
  Book    Journal     DVD             EBook
```

Why this hierarchy was chosen:

- Item types naturally differ in behavior (loan rules, type).
- These differences make them ideal for an "is-a" relationship.
- Cleanly extends Project 2 without rewriting other classes.

---

## 3. Abstract Base Class

The abstract base class is:

- AbstractLibraryItem

It requires all subclasses to implement:

- get_item_type()
- calculate_due_date(checkout_date, user_role)

This ensures consistency and demonstrates use of Python’s abc module.

---

## 4. Polymorphism

Each item subclass overrides inherited behaviors.

Examples of polymorphic behavior:

- Book: Standard 14/28-day due date
- Journal: Shorter 7/14-day due date
- DVD: Always 7 days
- EBook: Same-day digital due date (never overdue)

Also, each subclass returns its own string via get_item_type().

Calling the same method on each subclass produces different results, fulfilling the polymorphism requirement.

---

## 5. Composition

A new class, LibrarySystem, demonstrates composition.

LibrarySystem has:

- a Catalog
- a collection of Users
- a collection of Loans
- a collection of Holds

These are “has-a” relationships.

LibrarySystem coordinates:

- item checkout
- item return
- due-date calculation (via polymorphism)
- user management
- hold management

This shows composition clearly and satisfies the project requirement.

---

## 6. Integration With Project 2

Project 2 classes remain unchanged:

- User
- Loan
- Hold
- Catalog

These classes now work with the polymorphic item types and the LibrarySystem controller.

This follows the instruction to extend rather than rewrite Project 2.

---

## 7. Demonstration

The file demo_project3.py demonstrates:

- inheritance through creation of Book, Journal, DVD, and EBook
- polymorphism through calculate_due_date() and get_item_type()
- abstract class behavior
- composition through LibrarySystem
- a complete checkout workflow

The output is formatted in a clean section-based layout similar to the sample in the project instructions.

---

## 8. Testing

The test file test_project3.py verifies:

- the abstract class cannot be instantiated
- subclasses correctly inherit from LibraryItem and AbstractLibraryItem
- polymorphic due-date calculations
- composition checkout behavior in LibrarySystem

All tests pass.

---

## 9. Summary

This design:

- Adds a meaningful inheritance hierarchy
- Uses an abstract base class to enforce structure
- Demonstrates polymorphism clearly
- Implements composition through LibrarySystem
- Integrates with all Project 2 features
- Meets all requirements of the Project 3 specification

