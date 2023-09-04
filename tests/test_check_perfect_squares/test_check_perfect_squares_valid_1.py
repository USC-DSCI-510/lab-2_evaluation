import pytest

from lab2 import check_perfect_squares


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [({"tups": [(1, 1), (2, 4), (3, 9)]}, True, None)],
)
def test_check_perfect_squares(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            check_perfect_squares(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = check_perfect_squares(**input_args)
        assert result == expected_result
