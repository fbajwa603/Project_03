from __future__ import annotations
from datetime import date
from typing import Dict, List, Optional

from catalog import Catalog
from User import User
from libraryItem import LibraryItem
from loan import Loan
from Hold import Hold


class LibrarySystem:
    """
    Demonstrates composition:
        - LibrarySystem has-a Catalog
        - LibrarySystem has-a collection of Users
        - LibrarySystem has-a collection of Loans and Holds
    """

    def __init__(self, name: str):
        self._catalog = Catalog(name)
        self._users: Dict[str, User] = {}
        self._loans: Dict[str, Loan] = {}
        self._holds: Dict[str, Hold] = {}


    @property
    def catalog(self) -> Catalog:
        return self._catalog

    @property
    def users(self) -> Dict[str, User]:
        return self._users

    @property
    def loans(self) -> Dict[str, Loan]:
        return self._loans

    @property
    def holds(self) -> Dict[str, Hold]:
        return self._holds


    def add_user(self, user: User) -> None:
        if user.user_id in self._users:
            raise ValueError(f"User {user.user_id} already exists")
        self._users[user.user_id] = user

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)


    def add_item(self, item: LibraryItem) -> None:
        self._catalog.add_item(item)

    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        return self._catalog.get_item(item_id)


    def checkout_item(
        self,
        loan_id: str,
        user_id: str,
        item_id: str,
        checkout_date: date,
    ) -> Loan:
        """Create a loan using polymorphic item due-date rules."""
        user = self._users.get(user_id)
        if user is None:
            raise KeyError(f"Unknown user {user_id}")

        item = self._catalog.get_item(item_id)
        if item is None:
            raise KeyError(f"Unknown item {item_id}")

        if not item.is_available():
            raise RuntimeError(f"Item {item_id} is not available")

        due = item.calculate_due_date(checkout_date, user.role)

        item.checkout_copy()
        loan = Loan(loan_id, user.user_id, item.item_id, due)
        self._loans[loan_id] = loan
        user.add_loan(loan_id)
        return loan

    def return_item(
        self,
        loan_id: str,
        return_date: date,
        daily_rate: float = 0.25,
    ) -> float:
        """Return an item and apply any fines."""
        loan = self._loans.get(loan_id)
        if loan is None:
            raise KeyError(f"Unknown loan {loan_id}")

        item = self._catalog.get_item(loan.item_id)
        if item is None:
            raise KeyError(f"Unknown item {loan.item_id}")

        fine = loan.return_item(item, return_date, daily_rate)

        user = self._users[loan.user_id]
        user.remove_loan(loan_id)
        if fine > 0:
            user.add_fine(fine)

        return fine

    def place_hold(
        self,
        hold_id: str,
        user_id: str,
        item_id: str,
        placed_on: date,
        expires_on: date,
    ) -> Hold:
        """Create and store a new hold."""
        if hold_id in self._holds:
            raise ValueError(f"Hold {hold_id} already exists")
        hold = Hold(hold_id, user_id, item_id, placed_on, expires_on)
        self._holds[hold_id] = hold
        return hold

    def get_active_holds_for_item(self, item_id: str, today: date) -> List[Hold]:
        """Return all active holds for a given item."""
        return [
            h
            for h in self._holds.values()
            if h.item_id == item_id and h.is_active(today)
        ]
