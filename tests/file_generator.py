import os
import json
import subprocess


def serialize_tuples(obj):
    if isinstance(obj, tuple):
        return {"__tuple__": True, "items": obj}
    if isinstance(obj, list):
        return [serialize_tuples(item) for item in obj]
    if isinstance(obj, dict):
        return {key: serialize_tuples(value) for key, value in obj.items()}
    return obj


def serialize_string(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    return obj


def deserialize_tuples(obj):
    if isinstance(obj, list):
        return [deserialize_tuples(item) for item in obj]
    if isinstance(obj, dict):
        if "__tuple__" in obj:
            # Check if the items in the tuple are themselves dictionaries
            items = obj["items"]
            deserialized_items = [
                deserialize_tuples(item) if isinstance(item, dict) else item for item in items
            ]
            return tuple(deserialized_items)
        return {key: deserialize_tuples(value) for key, value in obj.items()}
    return obj


template = """import pytest

from lab2 import {function_name}


@pytest.mark.parametrize(
    'input_args, expected_result, exception_message',
    [
        ({test_cases}, {expected_result}, {exception_message})
    ]
)
def test_{function_name}(input_args, expected_result, exception_message):
    if exception_message is not None:
        with pytest.raises(Exception) as e_info:
            {function_name}(**input_args)
        assert str(e_info.value) == exception_message
    else:
        result = {function_name}(**input_args)
        assert result == expected_result
"""

DIR_PATH = os.path.dirname(__file__)
TEST_CONFIG_PATH = os.path.join(DIR_PATH, "config.json")

with open(TEST_CONFIG_PATH, "r") as f:
    config = deserialize_tuples(json.load(f))


# Loop through each test function in the configuration
for test_function_config in config["tests"]:
    function_name = test_function_config["test_function"]
    function_args_name = test_function_config["args_name"]

    # Define the output directory where you want to generate the test files
    OUTPUT_DIR = os.path.join(DIR_PATH, f"test_{function_name}")
    INIT_FILE_PATH = os.path.join(OUTPUT_DIR, "__init__.py")

    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(INIT_FILE_PATH):
        with open(INIT_FILE_PATH, "w") as init_file:
            pass

    test_cases = test_function_config["test_cases"]

    for test_case in test_cases:
        # Generate the test file content using the template
        test_file_content = template.format(
            function_name=function_name,
            test_cases=dict(zip(function_args_name, test_case["args"])),
            expected_result=serialize_string(test_case["expected_result"]),
            exception_message=serialize_string(test_case["exception_message"]),
        )

        # Write the test file content to a Python file
        TEST_CASE_FILE_NAME = test_case["name"]
        test_file_path = os.path.join(OUTPUT_DIR, f"{TEST_CASE_FILE_NAME}.py")

        with open(test_file_path, "w") as test_file:
            test_file.write(test_file_content)

    # Format the generated test file using black
    subprocess.run(["black", OUTPUT_DIR, "--preview", "--line-length=100", "--workers=2"])
