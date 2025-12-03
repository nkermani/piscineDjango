#!/usr/bin/env python3
from local_lib.path import Path


def main():
    # Create a directory
    test_dir = Path("./test_dir")
    test_dir.mkdir_p()  # mkdir_p creates parent dirs and doesn't fail if exists

    # Create and write to a file
    new_file = test_dir / "new_file.txt"  # Use / operator to join paths
    new_file.touch()
    new_file.write_text(
        "Hello, PathPy what a great day to work with you !\n\n\nnkermani\n42"
    )

    # Read the file
    content = new_file.read_text()
    print(content)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
