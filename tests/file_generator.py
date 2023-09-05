import os
import json
import subprocess
import multiprocessing


class SerializerDeserializer:
    """
    A utility class for serializing and deserializing objects.
    """

    @staticmethod
    def serialize_tuples(obj):
        """Serialize tuples within an object to a dictionary format."""
        if isinstance(obj, tuple):
            return {"__tuple__": True, "items": obj}
        if isinstance(obj, list):
            return [SerializerDeserializer.serialize_tuples(item) for item in obj]
        if isinstance(obj, dict):
            return {
                key: SerializerDeserializer.serialize_tuples(value) for key, value in obj.items()
            }
        return obj

    @staticmethod
    def serialize_string(obj):
        """Serialize a string by adding double quotes around it."""
        if isinstance(obj, str):
            return f'"{obj}"'
        return obj

    @staticmethod
    def deserialize_tuples(obj):
        """Deserialize a serialized object back into tuples."""
        if isinstance(obj, list):
            return [SerializerDeserializer.deserialize_tuples(item) for item in obj]
        if isinstance(obj, dict):
            if "__tuple__" in obj:
                # Check if the items in the tuple are themselves dictionaries
                items = obj["items"]
                deserialized_items = [
                    SerializerDeserializer.deserialize_tuples(item)
                    if isinstance(item, dict)
                    else item
                    for item in items
                ]
                return tuple(deserialized_items)
            return {
                key: SerializerDeserializer.deserialize_tuples(value) for key, value in obj.items()
            }
        return obj


class TestFileGenerator:
    def __init__(self, config_path, output_dir, template):
        """
        Initialize a TestFileGenerator instance.

        Args:
            config_path (str): Path to the JSON configuration file.
            output_dir (str): Directory where test files will be generated.
            template (str): Template for generating test files.
        """
        self.config_path = config_path
        self.output_dir = output_dir
        self.template = template

    def create_output_directory(self, output_dir):
        """Create the output directory if it doesn't exist."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def read_config(self):
        """Read and deserialize the JSON configuration file."""
        with open(self.config_path, "r") as f:
            return SerializerDeserializer.deserialize_tuples(json.load(f))

    def generate_test_case_content(self, function_name, function_args_name, test_case):
        """
        Generate the content for a test case file.

        Args:
            function_name (str): Name of the test function.
            function_args_name (list): Names of function arguments.
            test_case (dict): Test case configuration.

        Returns:
            str: Content of the test case file.
        """
        return self.template.format(
            function_name=function_name,
            test_cases=dict(zip(function_args_name, test_case["args"])),
            expected_result=SerializerDeserializer.serialize_string(test_case["expected_result"]),
            exception_message=SerializerDeserializer.serialize_string(
                test_case["exception_message"]
            ),
        )

    def write_test_case_file(self, output_dir, test_case_file_name, test_case_content):
        """
        Write the content of a test case file to disk.

        Args:
            output_dir (str): Directory where the test case file will be saved.
            test_case_file_name (str): Name of the test case file.
            test_case_content (str): Content of the test case file.
        """
        test_file_path = os.path.join(output_dir, f"{test_case_file_name}.py")
        with open(test_file_path, "w") as test_file:
            test_file.write(test_case_content)

    def format_test_case_files(self, output_dir):
        """Format the generated test case files using the black formatter."""
        num_workers = multiprocessing.cpu_count()
        print(f"Number of CPU cores available: {num_workers}")

        subprocess.run(
            ["black", output_dir, "--preview", "--line-length=100", f"--workers={num_workers}"]
        )

    def generate_test_files(self):
        """Generate test case files based on the configuration and format them."""
        config = self.read_config()

        for test_function_config in config["tests"]:
            function_name = test_function_config["test_function"]
            function_args_name = test_function_config["args_name"]

            # Define the output directory where you want to generate the test files
            output_dir = os.path.join(self.output_dir, f"test_{function_name}")
            self.create_output_directory(output_dir)

            # Create the __init__.py file for the test functions colleactions
            init_file_path = os.path.join(output_dir, "__init__.py")
            if not os.path.exists(init_file_path):
                with open(init_file_path, "w"):
                    pass

            for test_case in test_function_config["test_cases"]:
                test_case_file_name = test_case["name"]
                test_case_content = self.generate_test_case_content(
                    function_name, function_args_name, test_case
                )

                self.write_test_case_file(output_dir, test_case_file_name, test_case_content)

            self.format_test_case_files(output_dir)


class AutogradingConfigGenerator:
    def __init__(self, test_config_file, output_config_file):
        self.test_config_file = test_config_file
        self.output_config_file = output_config_file

    def read_config(self):
        """Read and deserialize the JSON configuration file."""
        with open(self.test_config_file, "r") as f:
            return json.load(f)

    def write_config(self, config):
        """Write the generated configuration to the output file."""
        with open(self.output_config_file, "w") as f:
            json.dump(config, f, indent=2)

    def generate_config(self):
        test_config = self.read_config()
        test_cases = []

        for test_function_config in test_config["tests"]:
            function_name = test_function_config["test_function"]
            test_suite_dir = f"test_{function_name}"
            # setup_command = "sudo -H pip3 install pytest"

            for test_case in test_function_config["test_cases"]:
                test_file = test_case["name"]
                test_cases.append(
                    {
                        "name": test_file,
                        # "setup": setup_command,
                        "run": f"pytest tests/{test_suite_dir}/{test_file}.py",
                        "timeout": 5,
                        "points": 1,
                    }
                )

        # Adding a bonus linting pass to the test suite
        test_cases.append(
            {
                "name": "bonus_pep8_linter_check_flake8",
                "run": (
                    "flake8 lab2.py --max-line-length=100"
                    " --ignore=E402,F841,F401,E302,E305,E266,E203,W503,E722"
                ),
                "timeout": 5,
                "points": 5,
            }
        )

        config = {"tests": test_cases}
        self.write_config(config)


if __name__ == "__main__":
    tests_directory = os.path.dirname(__file__)
    root_directory = os.path.dirname(tests_directory)
    test_config_path = os.path.join(tests_directory, "config.json")
    test_template_path = os.path.join(tests_directory, "test_template.txt")

    with open(test_template_path, "r") as f:
        test_template = f.read()

    test_file_generator = TestFileGenerator(test_config_path, tests_directory, test_template)
    test_file_generator.generate_test_files()

    # Output autograding config file
    output_config_file = os.path.join(root_directory, ".github", "classroom", "autograding.json")

    generator = AutogradingConfigGenerator(test_config_path, output_config_file)
    generator.generate_config()
