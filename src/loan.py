from datetime import date
from typing import List, Optional
from project_1_functions import calculate_due_date, compute_overdue_fine
from libraryItem import LibraryItem
from User import User
from Hold import Hold


class Loan:
    """Represents a checkout transaction between a user and item.
    
    Encapsulates loan data and integrates Project 1 functions for renewals,
    returns, and fine calculations.
    
    Attributes:
        loan_id: Unique loan identifier
        user_id: ID of borrowing user
        item_id: ID of borrowed item
        due: Due date
        returned_on: Return date (if applicable)
        renewals: Number of times renewed
    
    Example:
        >>> from datetime import date
        >>> loan = Loan("L001", "U001", "B001", date(2025, 11, 10))
        >>> loan.is_active()
        True
        >>> loan.is_overdue(date(2025, 11, 12))
        True
        >>> loan.calculate_fine(date(2025, 11, 15))
        1.25
    """

    def __init__(
        self,
        loan_id: str,
        user_id: str,
        item_id: str,
        due: date,
        returned_on: Optional[date] = None,
        renewals: int = 0,
    ):
        """Initialize a loan record.
        
        Args:
            loan_id: Unique loan identifier
            user_id: ID of user borrowing item
            item_id: ID of item being borrowed
            due: Due date
            returned_on: Return date (None if not returned)
            renewals: Number of times renewed
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not loan_id or not loan_id.strip():
            raise ValueError("Loan ID cannot be empty")
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        if not item_id or not item_id.strip():
            raise ValueError("Item ID cannot be empty")
        if renewals < 0:
            raise ValueError("Renewals cannot be negative")

        self._loan_id = loan_id.strip()
        self._user_id = user_id.strip()
        self._item_id = item_id.strip()
        self._due = due
        self._returned_on = returned_on
        self._renewals = renewals

    @property
    def loan_id(self) -> str:
        """Get the loan ID."""
        return self._loan_id

    @property
    def user_id(self) -> str:
        """Get the user ID."""
        return self._user_id

    @property
    def item_id(self) -> str:
        """Get the item ID."""
        return self._item_id

    @property
    def due(self) -> date:
        """Get the due date."""
        return self._due

    @property
    def returned_on(self) -> Optional[date]:
        """Get the return date if returned."""
        return self._returned_on

    @property
    def renewals(self) -> int:
        """Get the number of renewals."""
        return self._renewals

    def is_active(self) -> bool:
        """Check if loan is still active (not returned).
        
        Returns:
            True if item has not been returned
        """
        return self._returned_on is None

    def is_overdue(self, today: date) -> bool:
        """Check if loan is overdue.
        
        Args:
            today: Current date
            
        Returns:
            True if today is past due date and loan is active
        """
        return self.is_active() and today > self._due

    def days_overdue(self, today: date) -> int:
        """Calculate days overdue.
        
        Args:
            today: Current date
            
        Returns:
            Number of days overdue (0 if not overdue)
        """
        if not self.is_overdue(today):
            return 0
        return (today - self._due).days

    def days_until_due(self, today: date) -> int:
        """Calculate days until due date.
        
        Args:
            today: Current date
            
        Returns:
            Days remaining (0 if not active, negative if overdue)
        """
        if not self.is_active():
            return 0
        return (self._due - today).days

    def calculate_fine(self, return_date: date, daily_rate: float = 0.25) -> float:
        """Calculate fine using Project 1 function.
        
        Args:
            return_date: Date of return
            daily_rate: Fine per day overdue
            
        Returns:
            Fine amount
        """
        return compute_overdue_fine(self._due, return_date, daily_rate)

    def return_item(
        self,
        item: LibraryItem,
        return_date: date,
        daily_rate: float = 0.25,
    ) -> float:
        """Process return using Project 1 function logic.
        
        Args:
            item: LibraryItem being returned
            return_date: Date of return
            daily_rate: Fine per day overdue
            
        Returns:
            Fine amount (if any)
            
        Raises:
            RuntimeError: If already returned
        """
        if not self.is_active():
            raise RuntimeError(f"Loan {self._loan_id} is already closed")

        self._returned_on = return_date
        # Update item copies
        item.return_copy()

        fine = self.calculate_fine(return_date, daily_rate)
        if fine > 0:
            print(f"Returned late. Fine: ${fine:.2f}")
        else:
            print("Returned on time. No fine.")

        return fine

    def renew(
        self,
        user: User,
        item: LibraryItem,
        today: date,
        holds: Optional[List[Hold]] = None,
        max_renewals: int = 2,
        allow_overdue: bool = False,
    ) -> Optional[date]:
        """Renew loan using Project 1-style rules.
        
        Args:
            user: User renewing the loan
            item: Item being renewed
            today: Current date
            holds: List of holds to check against
            max_renewals: Maximum allowed renewals
            allow_overdue: Whether to allow renewal of overdue items
            
        Returns:
            New due date if successful, None otherwise
        """
        if not self.is_active():
            print("Cannot renew: item already returned.")
            return None

        if self._user_id != user.user_id:
            print("Cannot renew: different borrower.")
            return None

        if self._renewals >= max_renewals:
            print(f"Cannot renew: reached max renewals ({max_renewals}).")
            return None

        if not allow_overdue and today > self._due:
            print(f"Cannot renew: loan is overdue (due {self._due.isoformat()}).")
            return None

        if holds:
            for h in holds:
                if (
                    h.item_id == item.item_id
                    and h.user_id != user.user_id
                    and h.expires_on >= today
                    and not h.cancelled
                ):
                    print("Cannot renew: another patron has an active hold.")
                    return None

        self._due = calculate_due_date(today, user.role)
        self._renewals += 1
        print(
            f"Renewed. New due date: {self._due.isoformat()} "
            f"(renewals: {self._renewals}/{max_renewals})"
        )
        return self._due

    def __str__(self) -> str:
        status = "Active" if self.is_active() else f"Returned on {self._returned_on}"
        return f"Loan {self._loan_id}: Item {self._item_id} to User {self._user_id} - {status}"

    def __repr__(self) -> str:
        return (
            f"Loan(loan_id='{self._loan_id}', item_id='{self._item_id}', "
            f"user_id='{self._user_id}')"
        )
