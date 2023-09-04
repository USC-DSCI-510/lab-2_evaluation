import calendar
from datetime import datetime
from typing import List, Tuple


def format_date(day: int, month: int, year: int) -> str:
    # Check if the year is a leap year
    is_leap_year = calendar.isleap(year)

    # Validate the input date
    if not (1 <= day <= 31) or not (1 <= month <= 12) or not (1000 <= year <= 3000):
        raise Exception(f"The given date: {day}, {month}, {year} is invalid")

    # Check for the invalid date in February (non-leap year)
    if month == 2 and day > 28 and not is_leap_year:
        raise Exception(f"The given date: {day}, {month}, {year} is invalid")

    # Check for months with fewer than 31 days
    if (day > 30 and (month in [4, 6, 9, 11])) or (day > 31):
        raise Exception(f"The given date: {day}, {month}, {year} is invalid")

    # Create a datetime object with the provided components
    date_obj = datetime(year, month, day)

    # Format the date
    formatted_date = date_obj.strftime("%d %B, %Y")
    return formatted_date


def split_by_delimiter(some_string: str, delimiter: str) -> List[str]:
    # Check if input is valid
    if not isinstance(some_string, str) or not isinstance(delimiter, str):
        raise Exception("Invalid Input")

    # Handle the case of an empty delimiter
    if delimiter == "":
        return [some_string]

    # Split the string by the delimiter
    substrings = some_string.split(delimiter)
    return substrings


def check_perfect_squares(tups: List[Tuple]) -> bool:
    # Check if input is valid
    if not isinstance(tups, list) or not all(isinstance(t, tuple) and len(t) == 2 for t in tups):
        raise Exception("Invalid Input")

    # Check if each tuple is a perfect square pair
    for tup in tups:
        if not isinstance(tup[0], (int, float)) or not isinstance(tup[1], (int, float)):
            raise Exception("Invalid Input")
        if tup[0] * tup[0] != tup[1]:
            return False

    return True
