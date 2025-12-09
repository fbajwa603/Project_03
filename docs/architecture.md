1. Purpose

This project extends the Library Management System from Project 2 by adding:

Inheritance

Abstract Base Classes

Polymorphism

Composition

A coordinating class called LibrarySystem

The goal is to enhance the original system with advanced object-oriented design.

2. Inheritance Hierarchy

The inheritance structure centers around library items.

AbstractLibraryItem (ABC)
        |
        v
   LibraryItem
        |
   ---------------------------------------
   |        |         |                 |
  Book    Journal     DVD             EBook


Why this hierarchy was chosen:

Library items naturally differ in behavior (loan rules, type).

These differences make an “is-a” relationship appropriate.

This design fits the Project 3 requirement to refactor part of the system into a meaningful hierarchy.

3. Abstract Base Class

The abstract base class is:

AbstractLibraryItem

It defines required methods that every item subclass must implement:

get_item_type()

calculate_due_date(checkout_date, user_role)

This ensures consistent interfaces and demonstrates the use of Python’s abc module.

4. Polymorphism

Each item subclass overrides inherited methods to provide type-specific behavior.

Examples:

Books follow the default due-date rule (14 or 28 days).

Journals have shorter loan periods (7 or 14 days).

DVDs always use a 7-day loan period.

EBooks are due the same day and never become overdue.

Calling calculate_due_date() on different item types produces different results, even though the method name is the same.
This demonstrates polymorphism.

Each subclass also overrides get_item_type().

5. Composition

A new class, LibrarySystem, manages system-level interactions.

LibrarySystem has:

a Catalog

a collection of Users

a collection of Loans

a collection of Holds

These are “has-a” relationships, demonstrating composition.

LibrarySystem manages:

checking out items

returning items

due-date calculations (delegated polymorphically)

holds

catalog lookups

This class ties the entire system together without using inheritance.

6. Integration With Project 2

Project 2 classes remain unchanged:

User

Loan

Hold

Catalog

They work with the new system by using the polymorphic behavior of the updated item classes.

This follows the requirement to extend the previous project rather than replace it.

7. Demonstration

The file demo_project3.py demonstrates:

inheritance through item creation

polymorphism via calculate_due_date() and get_item_type()

abstract class rules

composition (LibrarySystem coordinating actions)

a working checkout workflow

The formatted output matches the sample style from the PDF.

8. Testing

The test file test_project3.py verifies:

ABC cannot be instantiated

subclasses correctly inherit from LibraryItem and AbstractLibraryItem

polymorphic due-date calculations

composition features of LibrarySystem

All tests pass.

9. Summary

This architecture:

Refactors part of the system into an inheritance hierarchy

Uses an abstract base class to enforce interfaces

Demonstrates polymorphism clearly

Adds composition with LibrarySystem

Fully integrates with all Project 2 functionality

Meets every requirement from the Project 3 PDF
