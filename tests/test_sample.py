import pytest

from lab2 import check_perfect_squares, format_date, split_by_delimiter


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [
        ({"day": 1, "month": 8, "year": 2000}, "01 August, 2000", None),
        ({"day": 30, "month": 13, "year": 2003}, None, "The given date: 30, 13, 2003 is invalid"),
    ],
)
def test_format_date(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            result = format_date(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = format_date(**input_args)
        assert result == expected_result


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [
        ({"some_string": 12, "delimiter": " "}, None, "Invalid Input"),
        ({"some_string": "1-2-3-4-5", "delimiter": "-"}, ["1", "2", "3", "4", "5"], None),
    ],
)
def test_split_by_delimiter(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            result = split_by_delimiter(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = split_by_delimiter(**input_args)
        assert result == expected_result


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [
        ({"tups": [(1, 1), (2, 4), (3, 9), (4, 15)]}, False, None),
        ({"tups": [("1, 1", (2, 4), (3, 9), (4, 16), (5, 25), (6, 36))]}, None, "Invalid Input"),
        ({"tups": [(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]}, True, None),
    ],
)
def test_check_perfect_squares(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            result = check_perfect_squares(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = check_perfect_squares(**input_args)
        assert result == expected_result
