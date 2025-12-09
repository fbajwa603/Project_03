from datetime import date, timedelta
from typing import List
from project_1_functions import validate_user_role, normalize_name, calculate_due_date


class User:
    """Represents a library user with borrowing privileges.
    
    Encapsulates user data with role validation and integrates Project 1 functions
    for due date calculation and name normalization.
    
    Attributes:
        user_id: Unique user identifier
        name: User's full name (normalized)
        role: User role (Student, Faculty, Staff, Admin, Public)
        active_loan_ids: List of currently active loan IDs
        total_fines: Outstanding fines amount
    
    Example:
        >>> user = User("U001", "jane doe", "Student")
        >>> user.name
        'Jane Doe'
        >>> user.get_loan_period()
        14
    """

    def __init__(self, user_id: str, name: str, role: str):
        """Initialize a library user with validation.
        
        Args:
            user_id: Unique identifier
            name: User's full name (will be normalized using Project 1 function)
            role: User role (validated using Project 1 function)
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        # Validate role using Project 1 function
        if not validate_user_role(role):
            raise ValueError(
                f"Invalid role: {role}. Must be Student, Faculty, Staff, Admin, or Public"
            )
        
        self._user_id = user_id.strip()
        # Normalize name using Project 1 function
        self._name = normalize_name(name)
        self._role = role
        self._active_loan_ids: List[str] = []
        self._total_fines = 0.0

    @property
    def user_id(self) -> str:
        """Get the user ID (read-only)."""
        return self._user_id

    @property
    def name(self) -> str:
        """Get the user's name."""
        return self._name

    @property
    def role(self) -> str:
        """Get the user's role."""
        return self._role

    @property
    def total_fines(self) -> float:
        """Get the total outstanding fines."""
        return self._total_fines

    def get_loan_period(self) -> int:
        """Get the loan period in days based on user role.
        
        Uses Project 1 logic: Students/Public get 14 days, others get 28 days.
        
        Returns:
            Number of days for loan period
        """
        return 14 if self._role in {"Student", "Public"} else 28

    def calculate_due_date(self, checkout_date: date) -> date:
        """Calculate due date for a checkout using Project 1 function.
        
        Args:
            checkout_date: Date of checkout
            
        Returns:
            Due date based on user's role
        """
        return calculate_due_date(checkout_date, self._role)

    def add_loan(self, loan_id: str) -> None:
        """Add a loan to user's active loans.
        
        Args:
            loan_id: ID of the loan to add
        """
        if loan_id not in self._active_loan_ids:
            self._active_loan_ids.append(loan_id)

    def remove_loan(self, loan_id: str) -> None:
        """Remove a loan from user's active loans.
        
        Args:
            loan_id: ID of the loan to remove
            
        Raises:
            ValueError: If loan not in active loans
        """
        if loan_id not in self._active_loan_ids:
            raise ValueError(f"Loan {loan_id} not found in active loans")
        self._active_loan_ids.remove(loan_id)

    def add_fine(self, amount: float) -> None:
        """Add a fine to user's account.
        
        Args:
            amount: Fine amount to add
            
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Fine amount cannot be negative")
        self._total_fines += amount

    def pay_fine(self, amount: float) -> float:
        """Pay down user's fines.
        
        Args:
            amount: Payment amount
            
        Returns:
            Remaining balance
            
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        self._total_fines = max(0, self._total_fines - amount)
        return self._total_fines

    def get_active_loan_count(self) -> int:
        """Get number of active loans."""
        return len(self._active_loan_ids)

    def has_fines(self) -> bool:
        """Check if user has outstanding fines."""
        return self._total_fines > 0

    def __str__(self) -> str:
        return f"{self._name} ({self._role}) - {len(self._active_loan_ids)} active loans"

    def __repr__(self) -> str:
        return (
            f"User(user_id='{self._user_id}', name='{self._name}', role='{self._role}')"
        )
