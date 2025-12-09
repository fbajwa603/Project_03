from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Optional, Set

from project_1_functions import (
    normalize_name,
    validate_isbn,
    check_item_availability,
    calculate_due_date as base_calculate_due_date,
)


class AbstractLibraryItem(ABC):
    """Abstract base class for all library items.

    This class defines the common interface that all concrete
    item types (Book, Journal, DVD, EBook, etc.) must implement.

    """

    @abstractmethod
    def get_item_type(self) -> str:
        """Return a short human-readable type label (e.g., 'Book', 'DVD')."""
        raise NotImplementedError

    @abstractmethod
    def calculate_due_date(self, checkout_date: date, user_role: str) -> date:
        """Calculate the due date for this item given the user's role.

        Subclasses implement different policies to demonstrate polymorphism.
        """
        raise NotImplementedError


class LibraryItem(AbstractLibraryItem):
    """Represents a generic item in a library catalog with controlled access.

    Encapsulates item data with validation and integrates Project 1 functions
    for availability checking and searching.

    Attributes:
        item_id: Unique identifier for the item
        title: Title of the item
        creators: List of authors/creators (normalized)
        tags: Set of subject tags
        available_copies: Number of available copies
        call_number: Optional call number for shelving"""

    def __init__(
        self,
        item_id: str,
        title: str,
        creators: List[str],
        tags: Set[str],
        available_copies: int,
        call_number: Optional[str] = None,
        isbn: Optional[str] = None,
    ):
        """Initialize a library item with validation."""
        if not item_id or not item_id.strip():
            raise ValueError("Item ID cannot be empty")
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if available_copies < 0:
            raise ValueError("Available copies cannot be negative")
        if isbn and not validate_isbn(isbn):
            raise ValueError(f"Invalid ISBN: {isbn}")

        self._item_id = item_id.strip()
        self._title = title.strip()
        self._creators = [normalize_name(c) for c in creators] if creators else []
        self._tags = set(tags) if tags else set()
        self._available_copies = int(available_copies)
        self._total_copies = int(available_copies)
        self._call_number = call_number.strip() if call_number else None
        self._isbn = isbn


    @property
    def item_id(self) -> str:
        """Get the item ID (read-only)."""
        return self._item_id

    @property
    def title(self) -> str:
        """Get the item title."""
        return self._title

    @property
    def creators(self) -> List[str]:
        """Get the list of creators."""
        return self._creators.copy()

    @property
    def tags(self) -> Set[str]:
        """Get the set of tags."""
        return self._tags.copy()

    @property
    def available_copies(self) -> int:
        """Get number of available copies."""
        return self._available_copies

    @property
    def call_number(self) -> Optional[str]:
        """Get the call number."""
        return self._call_number


    def get_item_type(self) -> str:
        """Default type label for generic items.

        Subclasses override this to demonstrate polymorphism.
        """
        return "Generic Item"

    def calculate_due_date(self, checkout_date: date, user_role: str) -> date:
        """Default due-date policy using Project 1 helper.

        Students/Public: 14 days
        Faculty/Staff/Admin: 28 days
        """
        return base_calculate_due_date(checkout_date, user_role)


    def check_availability(self) -> bool:
        """Check and print item availability using Project 1 function.

        Returns:
            True if at least one copy is available
        """
        return check_item_availability(self)

    def is_available(self) -> bool:
        """Check if any copies are available (silent version)."""
        return self._available_copies > 0

    def checkout_copy(self) -> None:
        """Check out one copy of the item."""
        if self._available_copies <= 0:
            raise RuntimeError(f"Item {self._item_id} has no available copies")
        self._available_copies -= 1

    def return_copy(self) -> None:
        """Return one copy of the item."""
        if self._available_copies >= self._total_copies:
            raise RuntimeError(
                f"All copies of {self._item_id} are already returned"
            )
        self._available_copies += 1


    def add_tag(self, tag: str) -> None:
        """Add a subject tag to the item."""
        if tag and tag.strip():
            self._tags.add(tag.strip().lower())

    def remove_tag(self, tag: str) -> None:
        """Remove a subject tag from the item."""
        self._tags.discard(tag.strip().lower())

    def has_tag(self, tag: str) -> bool:
        """Check if item has a specific tag."""
        return tag.strip().lower() in self._tags

    def __str__(self) -> str:
        creators_str = ", ".join(self._creators) if self._creators else "Unknown"
        return f"{self._title} by {creators_str} - {self._available_copies} available"

    def __repr__(self) -> str:
        return (
            f"LibraryItem(item_id='{self._item_id}', "
            f"title='{self._title}', available={self._available_copies})"
        )


class Book(LibraryItem):
    """Concrete book item.

    Inherits all fields from LibraryItem, but provides a specific type label.
    """

    def __init__(
        self,
        item_id: str,
        title: str,
        creators: List[str],
        tags: Set[str],
        available_copies: int,
        call_number: Optional[str] = None,
        isbn: Optional[str] = None,
        genre: Optional[str] = None,
    ):
        super().__init__(item_id, title, creators, tags, available_copies,
                         call_number=call_number, isbn=isbn)
        self._genre = genre

    @property
    def genre(self) -> Optional[str]:
        return self._genre

    def get_item_type(self) -> str:
        return "Book"



class Journal(LibraryItem):
    """Journal or periodical item.

    Example specialized rule: journals have slightly shorter loan periods.
    """

    def get_item_type(self) -> str:
        return "Journal"

    def calculate_due_date(self, checkout_date: date, user_role: str) -> date:
        # Students/Public: 7 days, others: 14 days
        days = 7 if user_role in {"Student", "Public"} else 14
        return checkout_date + timedelta(days=days)


class DVD(LibraryItem):
    """DVD / video item with short-term checkout."""

    def get_item_type(self) -> str:
        return "DVD"

    def calculate_due_date(self, checkout_date: date, user_role: str) -> date:
        # All roles: 7-day checkout for DVDs.
        return checkout_date + timedelta(days=7)


class EBook(LibraryItem):
    """Electronic book item.

    Demonstrates a very different circulation model:
    - Access is immediate and may not accrue overdue fines in the same way.
    """

    def get_item_type(self) -> str:
        return "EBook"

    def calculate_due_date(self, checkout_date: date, user_role: str) -> date:
        return checkout_date

    def checkout_copy(self) -> None:
        """Override to avoid decrementing physical copy counts.

        EBooks are licensed resources; assume unlimited concurrent access
        for this project.
        """

        pass
