import pytest

from lab2 import format_date, split_by_delimiter, check_perfect_squares


# pytest cases
def test_format_date():
    assert format_date(1, 8, 2000) == "01 August, 2000"
    assert format_date(27, 1, 2003) == "27 January, 2003"
    assert format_date(7, 8, 2000) == "07 August, 2000"

    with pytest.raises(Exception) as e_info:
        format_date(32, 1, 2003)
    assert str(e_info.value) == "The given date: 32, 1, 2003 is invalid"

    with pytest.raises(Exception) as e_info:
        format_date(30, 13, 2003)
    assert str(e_info.value) == "The given date: 30, 13, 2003 is invalid"

    with pytest.raises(Exception) as e_info:
        format_date(29, 2, 2003)
    assert str(e_info.value) == "The given date: 29, 2, 2003 is invalid"


def test_split_by_delimiter():
    assert split_by_delimiter("a,b,c", ",") == ["a", "b", "c"]
    assert split_by_delimiter("a b c", " ") == ["a", "b", "c"]
    assert split_by_delimiter("a,b,c", " ") == ["a,b,c"]
    assert split_by_delimiter("a,b,c", "") == ["a,b,c"]

    with pytest.raises(Exception) as e_info:
        split_by_delimiter(12, " ")
    assert str(e_info.value) == "Invalid Input"

    with pytest.raises(Exception) as e_info:
        split_by_delimiter("a,b,c", 12)
    assert str(e_info.value) == "Invalid Input"


def test_check_perfect_squares():
    assert check_perfect_squares([(1, 1), (2, 4), (3, 9)])
    assert not check_perfect_squares([(1, 1), (2, 4), (3, 8)])
    assert check_perfect_squares([(1, 1), (2, 4), (3, 9), (4, 16)])
    assert not check_perfect_squares([(1, 1), (2, 4), (3, 9), (4, 15)])
    assert check_perfect_squares([(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)])

    with pytest.raises(Exception) as e_info:
        check_perfect_squares(["1, 1", (2, 4), (3, 9), (4, 16), (5, 25), (6, 36)])
    assert str(e_info.value) == "Invalid Input"

    with pytest.raises(Exception) as e_info:
        check_perfect_squares([1, 1, 2, 2])
    assert str(e_info.value) == "Invalid Input"
    with pytest.raises(Exception) as e_info:
        check_perfect_squares((1, 1))
    assert str(e_info.value) == "Invalid Input"
    with pytest.raises(Exception) as e_info:
        check_perfect_squares([(1, 1, 1), (2, 2, 2)])
    assert str(e_info.value) == "Invalid Input"
