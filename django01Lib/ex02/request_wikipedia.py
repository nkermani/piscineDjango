import sys
import dewiki
import requests


def clean_wiki_content(content):
    while "<ref" in content.lower():
        start = content.lower().find("<ref")
        if start == -1:
            break
        # Check if it's self-closing <ref ... />
        end_bracket = content.find(">", start)
        if end_bracket != -1 and content[end_bracket - 1] == "/":
            content = content[:start] + content[end_bracket + 1 :]
        else:
            # Find closing </ref>
            end = content.lower().find("</ref>", start)
            if end != -1:
                content = content[:start] + content[end + 6 :]
            else:
                break

    search_start = 0
    while True:
        start = content.lower().find("{{infobox", search_start)
        if start == -1:
            break
        # Skip the entire infobox by counting braces
        depth = 2
        j = start + 2
        while j < len(content) and depth > 0:
            if content[j : j + 2] == "{{":
                depth += 2
                j += 2
            elif content[j : j + 2] == "}}":
                depth -= 2
                j += 2
            else:
                j += 1
        content = content[:start] + content[j:]

    # Convert MediaWiki markup to plain text
    plain_text = dewiki.from_string(content)

    # Clean up extra whitespace
    lines = plain_text.split("\n")
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        line = line.strip()
        if line == "":
            if not prev_empty:
                cleaned_lines.append("")
            prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False

    return "\n".join(cleaned_lines).strip()


def search_wikipedia(query):
    """Search Wikipedia and return the page content if found."""
    url = "https://en.wikipedia.org/w/api.php"

    # First, search for the term (handles misspellings via Wikipedia's search)
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
    }

    user_agent = {"User-Agent": "Mozilla/5.0 (compatible; MyWikipediaBot/1.0)"}

    response = requests.get(url, params=search_params, headers=user_agent)
    response.raise_for_status()

    data = response.json()

    if not data["query"]["search"]:
        return None, "No results found for this search."

    # Get the title of the first result
    title = data["query"]["search"][0]["title"]

    # Now fetch the content of that page
    content_params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "rvprop": "content",
        "titles": title,
        "formatversion": "2",
    }

    response = requests.get(url, params=content_params, headers=user_agent)
    response.raise_for_status()

    data = response.json()
    page = data["query"]["pages"][0]

    if "missing" in page:
        return None, "Page not found."

    content = page["revisions"][0]["content"]

    # Clean and convert MediaWiki markup to plain text
    plain_text = clean_wiki_content(content)

    return plain_text, title


def main():
    if len(sys.argv) != 2:
        print("Usage: python request_wikipedia.py <search_term>", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1].strip()

    if not query:
        print("Error: Search term cannot be empty.", file=sys.stderr)
        sys.exit(1)

    try:
        content, result = search_wikipedia(query)

        if content is None:
            print(f"Error: {result}", file=sys.stderr)
            sys.exit(1)

        # Create filename: replace spaces with underscores, add .wiki extension
        filename = query.replace(" ", "_") + ".wiki"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Content saved to {filename}")

    except requests.exceptions.ConnectionError:
        print(
            "Error: Unable to connect to Wikipedia. Check your internet connection.",
            file=sys.stderr,
        )
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request timed out.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: Server error ({e.response.status_code}).", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
