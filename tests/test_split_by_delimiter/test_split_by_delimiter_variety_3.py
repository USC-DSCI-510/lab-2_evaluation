import pytest

from lab2 import split_by_delimiter


@pytest.mark.parametrize(
    "input_args, expected_result, exception_message",
    [({"some_string": "1-2-3-4-5", "delimiter": "-"}, ["1", "2", "3", "4", "5"], None)],
)
def test_split_by_delimiter(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            split_by_delimiter(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = split_by_delimiter(**input_args)
        assert result == expected_result
