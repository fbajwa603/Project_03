from typing import List, Dict, Optional, Set
from libraryItem import LibraryItem
from project_1_functions import search_items


class Catalog:
    """Manages the library's collection of items.
    
    Encapsulates catalog operations and integrates Project 1 search functionality.
    
    Attributes:
        name: Name of the catalog
        items: Dictionary of items indexed by item_id
    
    Example:
        >>> catalog = Catalog("Main Library")
        >>> item = LibraryItem("B001", "Python Guide", ["Guido"], {"programming"}, 3)
        >>> catalog.add_item(item)
        >>> catalog.search_by_keyword("Python")
        Found 1 item(s) matching 'Python':
        - Python Guide (Guido)
    """

    def __init__(self, name: str):
        """Initialize a catalog.
        
        Args:
            name: Name of the catalog
            
        Raises:
            ValueError: If name is empty
        """
        if not name or not name.strip():
            raise ValueError("Catalog name cannot be empty")

        self._name = name.strip()
        self._items: Dict[str, LibraryItem] = {}

    @property
    def name(self) -> str:
        """Get the catalog name."""
        return self._name

    @property
    def item_count(self) -> int:
        """Get total number of items in catalog."""
        return len(self._items)

    def add_item(self, item: LibraryItem) -> None:
        """Add an item to the catalog.
        
        Args:
            item: LibraryItem to add
            
        Raises:
            ValueError: If item already exists
        """
        if item.item_id in self._items:
            raise ValueError(f"Item {item.item_id} already exists in catalog")
        self._items[item.item_id] = item

    def remove_item(self, item_id: str) -> LibraryItem:
        """Remove an item from the catalog.
        
        Args:
            item_id: ID of item to remove
            
        Returns:
            The removed item
            
        Raises:
            KeyError: If item not found
        """
        if item_id not in self._items:
            raise KeyError(f"Item {item_id} not found in catalog")
        return self._items.pop(item_id)

    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        """Retrieve an item by ID.
        
        Args:
            item_id: ID of item to retrieve
            
        Returns:
            LibraryItem if found, None otherwise
        """
        return self._items.get(item_id)

    def list_all_items(self) -> List[LibraryItem]:
        """Return a list of all items in the catalog."""
        return list(self._items.values())

    def search_by_keyword(self, keyword: str) -> List[LibraryItem]:
        """Search for items by keyword using Project 1 search_items.
        
        Args:
            keyword: Keyword to search for in titles
            
        Returns:
            List of matching items
        """
        items_list = list(self._items.values())
        return search_items(items_list, keyword)

    def search_by_creator(self, creator: str) -> List[LibraryItem]:
        """Search for items by creator name (case-insensitive partial match).
        
        Args:
            creator: Creator name or partial name to search for
            
        Returns:
            List of matching items
        """
        creator_lower = creator.lower()
        results = [
            item
            for item in self._items.values()
            if any(creator_lower in c.lower() for c in item.creators)
        ]
        return results

    def __str__(self) -> str:
        return f"Catalog '{self._name}' with {self.item_count} item(s)"

    def __repr__(self) -> str:
        return f"Catalog(name='{self._name}', items={self.item_count})"