import sys
import os


def render_template(template_file):
    """
    Reads a .template file, replaces placeholders with values from settings.py,
    and writes the result to a .html file.
    """
    # Check if file has .template extension
    if not template_file.endswith(".template"):
        print("Error: File must have .template extension")
        sys.exit(1)

    # Check if file exists
    if not os.path.exists(template_file):
        print(f"Error: File '{template_file}' does not exist")
        sys.exit(1)

    # Read the template file
    try:
        with open(template_file, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Import settings to get replacement values
    try:
        import settings
    except ImportError:
        print("Error: settings.py not found")
        sys.exit(1)

    # Get all variables from settings module
    settings_vars = {
        key: value for key, value in vars(settings).items() if not key.startswith("_")
    }

    # Replace placeholders in content
    try:
        rendered_content = content.format(**settings_vars)
    except KeyError as e:
        print(f"Error: Missing variable in settings.py: {e}")
        sys.exit(1)

    # Generate output filename
    output_file = template_file.replace(".template", ".html")

    # Write to output file
    try:
        with open(output_file, "w") as f:
            f.write(rendered_content)
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check number of arguments
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <file.template>")
        sys.exit(1)

    template_file = sys.argv[1]
    render_template(template_file)
