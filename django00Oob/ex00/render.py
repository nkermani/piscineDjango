#!/usr/bin/env python3

import sys
import os


def render_template(template_file):
    if not template_file.endswith(".template"):
        print("Error: File must have .template extension")
        sys.exit(1)

    if not os.path.exists(template_file):
        print(f"Error: File '{template_file}' does not exist")
        sys.exit(1)

    try:
        with open(template_file, "r") as f:
            content = f.read()
            if not content:
                print("Error: Template file is empty")
                sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    try:
        import settings
    except ImportError:
        print("Error: settings.py not found")
        sys.exit(1)

    settings_vars = {
        key: value for key, value in vars(settings).items() if not key.startswith("_")
    }

    try:
        rendered_content = content.format(**settings_vars)
    except KeyError as e:
        print(f"Error: Missing variable in settings.py: {e}")
        sys.exit(1)

    output_file = template_file.replace(".template", ".html")

    try:
        with open(output_file, "w") as f:
            f.write(rendered_content)
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <file.template>")
        sys.exit(1)

    template_file = sys.argv[1]
    render_template(template_file)


if __name__ == "__main__":
    main()
