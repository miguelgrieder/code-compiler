import sys


def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file ({file_path}) doesn't exist!", flush=True)  # noqa: T201
        sys.exit(1)
    else:
        return file_content
