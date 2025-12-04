import sys
import requests
from bs4 import BeautifulSoup


def get_page_info(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RoadsToPhilosophy/1.0)"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", {"id": "firstHeading"})
    title = title_tag.get_text(strip=True) if title_tag else None

    redirect_notice = soup.find("div", {"class": "mw-content-subtitle"})
    redirect_from = None
    if redirect_notice:
        redirect_link = redirect_notice.find("a")
        if redirect_link and "Redirected from" in redirect_notice.get_text():
            redirect_from = redirect_link.get_text(strip=True)

    return soup, title, redirect_from


def get_first_link(soup):
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return None

    parser_output = content.find("div", {"class": "mw-parser-output"})
    if not parser_output:
        return None

    paragraphs = parser_output.find_all("p")

    for paragraph in paragraphs:
        parent = paragraph.parent
        skip = False
        while parent and parent != parser_output:
            if parent.name == "table":
                skip = True
                break
            parent_class = parent.get("class", [])
            if parent_class and any(
                "infobox" in c or "sidebar" in c or "navbox" in c for c in parent_class
            ):
                skip = True
                break
            parent = parent.parent
        if skip:
            continue

        if not paragraph.get_text(strip=True):
            continue

        paragraph_html = str(paragraph)

        for link in paragraph.find_all("a", href=True):
            href = link.get("href", "")

            if not href.startswith("/wiki/"):
                continue

            if ":" in href.split("/wiki/")[1]:
                continue

                continue

            link_html = str(link)
            link_pos = paragraph_html.find(link_html)
            if link_pos != -1:
                text_before = paragraph_html[:link_pos]
                clean_text = ""
                in_tag = False
                for char in text_before:
                    if char == "<":
                        in_tag = True
                    elif char == ">":
                        in_tag = False
                    elif not in_tag:
                        clean_text += char
                open_parens = clean_text.count("(") - clean_text.count(")")
                if open_parens > 0:
                    continue

            parent = link.parent
            is_italic = False
            while parent and parent != paragraph:
                if parent.name in ["i", "em"]:
                    is_italic = True
                    break
                parent = parent.parent
            if is_italic:
                continue

            return href

    return None


def roads_to_philosophy(search_term):
    base_url = "https://en.wikipedia.org/wiki/"
    search_term_formatted = search_term.replace(" ", "_")
    current_url = base_url + search_term_formatted

    visited = []

    while True:
        try:
            soup, title, redirect_from = get_page_info(current_url)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("It leads to a dead end!")
            else:
                print(f"Error: Server error ({e.response.status_code}).")
            return
        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to Wikipedia.")
            return
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        if not title:
            print("It leads to a dead end!")
            return

        if redirect_from and redirect_from not in visited:
            visited.append(redirect_from)
            print(redirect_from)

        if title in visited:
            print(title)
            print("It leads to an infinite loop!")
            return

        visited.append(title)
        print(title)

        if title.lower() == "philosophy":
            print(f"{len(visited)} roads from {search_term} to philosophy!")
            return

        next_href = get_first_link(soup)

        if not next_href:
            print("It leads to a dead end!")
            return

        current_url = "https://en.wikipedia.org" + next_href


def main():
    if len(sys.argv) != 2:
        print("Usage: python roads_to_philosophy.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1].strip()

    if not search_term:
        print("Error: Search term cannot be empty.")
        sys.exit(1)
    roads_to_philosophy(search_term)


if __name__ == "__main__":
    main()
