import pytest

from lab2 import format_date


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [({"day": 29, "month": 2, "year": 2021}, None, "The given date: 29, 2, 2021 is invalid")],
)
def test_format_date(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            format_date(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = format_date(**input_args)
        assert result == expected_result
