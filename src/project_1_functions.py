from datetime import date, timedelta

# Validate that the role assigned to the user is permitted
def validate_user_role(role):
    """Return True if role is valid; else False."""
    return role in {"Student", "Faculty", "Staff", "Admin", "Public"}

def search_items(items, keyword):
    """Search items by keyword in title and print matches."""
    results = [i for i in items if keyword.lower() in i.title.lower()]
    print(f"Found {len(results)} item(s) matching '{keyword}':")
    for i in results:
        print(f"- {i.title} ({', '.join(i.creators)})")
    return results

def normalize_name(name):
    """Normalize a name string (strip spaces and title-case)."""
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return " ".join(name.strip().split()).title()

def parse_date_yyyy_mm_dd(s):
    """Convert ISO-format string (YYYY-MM-DD) to date object."""
    try:
        return date.fromisoformat(s)
    except Exception as e:
        raise ValueError(f"Invalid date '{s}': {e}")

def validate_isbn(isbn):
    """Validate ISBN-10 or ISBN-13 number."""
    s = isbn.replace("-", "").replace(" ", "").upper()
    if len(s) == 10:
        total = 0
        for i, ch in enumerate(s):
            if ch == "X":
                if i != 9:
                    return False
                val = 10
            else:
                if not ch.isdigit():
                    return False
                val = int(ch)
            total += (10 - i) * val
        return total % 11 == 0
    elif len(s) == 13 and s.isdigit():
        total = 0
        for i, d in enumerate(s):
            w = 1 if i % 2 == 0 else 3
            total += w * int(d)
        return total % 10 == 0
    return False

def calculate_due_date(start, role):
    """Calculate due date based on user role (14 or 28 days)."""
    days = 14 if role in {"Student", "Public"} else 28
    return start + timedelta(days=days)

def check_item_availability(item):
    """Print and return availability of an item."""
    if item.available_copies > 0:
        print(f"'{item.title}' is available ({item.available_copies} copies).")
        return True
    else:
        print(f"'{item.title}' is currently unavailable.")
        return False
    
def compute_overdue_fine(due_date, return_date, daily_rate=0.25):
    """Compute fine based on days overdue."""
    if return_date <= due_date:
        return 0.0
    days_late = (return_date - due_date).days
    return round(days_late * daily_rate, 2)

