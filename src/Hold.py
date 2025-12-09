from datetime import date, timedelta


class Hold:
    """Represents a hold/reservation for an item.
    
    Encapsulates hold data with expiration tracking and notification status.
    
    Attributes:
        hold_id: Unique hold identifier
        user_id: ID of user placing hold
        item_id: ID of item on hold
        placed_on: Date hold was placed 
        expires_on: Date hold expires
        notified: Whether user has been notified
    
    Example:
        >>> from datetime import date
        >>> hold = Hold("H001", "U001", "B001",
        ...             date(2025, 11, 1), date(2025, 11, 7))
        >>> hold.is_active(date(2025, 11, 3))
        True
    """

    def __init__(
        self,
        hold_id: str,
        user_id: str,
        item_id: str,
        placed_on: date,
        expires_on: date,
        notified: bool = False,
    ):
        """Initialize a hold.
        
        Args:
            hold_id: Unique identifier
            user_id: ID of user placing hold
            item_id: ID of item on hold
            placed_on: Date hold was placed
            expires_on: Date hold expires
            notified: Whether user has been notified
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not hold_id or not hold_id.strip():
            raise ValueError("Hold ID cannot be empty")
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        if not item_id or not item_id.strip():
            raise ValueError("Item ID cannot be empty")
        if expires_on < placed_on:
            raise ValueError("Expiry date cannot be before placement date")

        self._hold_id = hold_id.strip()
        self._user_id = user_id.strip()
        self._item_id = item_id.strip()
        self._placed_on = placed_on
        self._expires_on = expires_on
        self._notified = bool(notified)
        self._fulfilled = False
        self._cancelled = False

    @property
    def hold_id(self) -> str:
        """Get hold ID."""
        return self._hold_id

    @property
    def user_id(self) -> str:
        """Get user ID."""
        return self._user_id

    @property
    def item_id(self) -> str:
        """Get item ID."""
        return self._item_id

    @property
    def placed_on(self) -> date:
        """Get placement date."""
        return self._placed_on

    @property
    def expires_on(self) -> date:
        """Get expiry date."""
        return self._expires_on

    @property
    def notified(self) -> bool:
        """Whether user has been notified."""
        return self._notified

    @property
    def fulfilled(self) -> bool:
        """Whether the hold is fulfilled."""
        return self._fulfilled

    @property
    def cancelled(self) -> bool:
        """Whether the hold is cancelled."""
        return self._cancelled

    def is_active(self, today: date) -> bool:
        """Check if hold is currently active.
        
        Args:
            today: Current date
            
        Returns:
            True if not fulfilled/cancelled and not past expiry
        """
        return (
            not self._fulfilled
            and not self._cancelled
            and today <= self._expires_on
        )

    def is_expired(self, today: date) -> bool:
        """Check if hold has expired.
        
        Args:
            today: Current date
            
        Returns:
            True if past expiry date and not fulfilled
        """
        return not self._fulfilled and today > self._expires_on

    def notify(self) -> None:
        """Mark user as notified.
        
        Raises:
            RuntimeError: If hold is fulfilled or cancelled
        """
        if self._fulfilled or self._cancelled:
            raise RuntimeError(f"Hold {self._hold_id} is not active")
        self._notified = True
        print(f"User {self._user_id} notified about hold {self._hold_id}")

    def fulfill(self) -> None:
        """Mark hold as fulfilled (item checked out).
        
        Raises:
            RuntimeError: If hold is cancelled
        """
        if self._cancelled:
            raise RuntimeError(f"Hold {self._hold_id} is cancelled")
        self._fulfilled = True
        print(f"Hold {self._hold_id} fulfilled")

    def cancel(self) -> None:
        """Cancel the hold.
        
        Raises:
            RuntimeError: If hold already fulfilled
        """
        if self._fulfilled:
            raise RuntimeError("Cannot cancel fulfilled hold")
        self._cancelled = True
        print(f"Hold {self._hold_id} cancelled")

    def days_until_expiry(self, today: date) -> int:
        """Calculate days until hold expires.
        
        Args:
            today: Current date
            
        Returns:
            Days until expiry (0 if inactive, negative if past expiry)
        """
    def days_until_expiry(self, today: date) -> int:
        """Days until expiry (0 if fulfilled/cancelled, negative if past expiry)."""
        if self._fulfilled or self._cancelled:
            return 0
        return (self._expires_on - today).days


    def extend(self, additional_days: int, today: date) -> date:
        """Extend an active hold by a given number of days.
        
        Args:
            additional_days: Number of days to extend
            today: Current date
            
        Returns:
            New expiry date
            
        Raises:
            RuntimeError: If hold is not active
            ValueError: If additional_days is invalid
        """
        if not self.is_active(today):
            raise RuntimeError("Cannot extend inactive hold")
        if additional_days < 1:
            raise ValueError("Extension must be at least 1 day")
        self._expires_on = self._expires_on + timedelta(days=additional_days)
        return self._expires_on

    def __str__(self) -> str:
        """Human-readable string representation of the hold."""
        status = (
            "Active"
            if not (self._fulfilled or self._cancelled)
            else ("Fulfilled" if self._fulfilled else "Cancelled")
        )
        notif = " (Notified)" if self._notified else ""
        return (
            f"Hold {self._hold_id}: Item {self._item_id} "
            f"for User {self._user_id} - {status}{notif}"
        )

    def __repr__(self) -> str:
        """Debug representation of the hold."""
        return (
            f"Hold(hold_id='{self._hold_id}', "
            f"item_id='{self._item_id}', user_id='{self._user_id}')"
        )
