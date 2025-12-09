# Library Management System – Project 3 (Short README)

## Overview
This project extends the Project 2 Library System by adding:

- Inheritance
- Abstract Base Classes (ABC)
- Polymorphism
- Composition
- A new controller class (`LibrarySystem`)
- A formatted demonstration script
- Automated tests

The system keeps all Project 2 functionality and builds advanced OOP features on top of it.

---

## Inheritance Structure
```
AbstractLibraryItem (ABC)
       ↓
   LibraryItem
       ↓
  Book | Journal | DVD | EBook
```

Each item type implements different due-date rules and behaviors.

---

## Abstract Base Class
`AbstractLibraryItem` requires:

- `get_item_type()`
- `calculate_due_date()`

All subclasses implement these methods.

---

## Polymorphism
Different item types respond differently to the same method:

- Books → standard loan rules  
- Journals → shorter loans  
- DVDs → fixed 7-day loan  
- EBooks → same-day digital due date  

---

## Composition
`LibrarySystem` is a coordinating class that:

- has a Catalog  
- has Users  
- has Loans  
- has Holds  

It handles checkouts, returns, and user interactions.

---

## Running the Demo
From the `src/` directory:

```
python demo_project3.py
```

---

## Running Tests
```
python test_project3.py
```

All tests should pass.

---

## Summary
This project adds:

- a meaningful inheritance hierarchy  
- an abstract base class  
- polymorphic behaviors  
- composition through LibrarySystem  
- full integration with Project 2  
