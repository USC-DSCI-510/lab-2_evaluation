import pytest

from lab2 import format_date


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [({"day": 0, "month": 5, "year": 2005}, None, "The given date: 0, 5, 2005 is invalid")],
)
def test_format_date(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            format_date(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = format_date(**input_args)
        assert result == expected_result
