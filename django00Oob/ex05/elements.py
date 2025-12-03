#!/usr/bin/env python3
from elem import Elem, Text


# Specific HTML elements as subclasses of Elem
# Document-related elements
class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="html", attr=attr, content=content, tag_type="double")


class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="head", attr=attr, content=content, tag_type="double")


class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="body", attr=attr, content=content, tag_type="double")


# Title element
class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="title", attr=attr, content=content, tag_type="double")


# Meta and Img elements
class Meta(Elem):
    def __init__(self, attr={}):
        super().__init__(tag="meta", attr=attr, content=None, tag_type="simple")


class Img(Elem):
    def __init__(self, attr={}):
        super().__init__(tag="img", attr=attr, content=None, tag_type="simple")


#  Table-related elements
class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="table", attr=attr, content=content, tag_type="double")


class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="th", attr=attr, content=content, tag_type="double")


class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="tr", attr=attr, content=content, tag_type="double")


class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="td", attr=attr, content=content, tag_type="double")


# List-related elements


class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="ul", attr=attr, content=content, tag_type="double")


class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="ol", attr=attr, content=content, tag_type="double")


class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="li", attr=attr, content=content, tag_type="double")


class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="h1", attr=attr, content=content, tag_type="double")


class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="h2", attr=attr, content=content, tag_type="double")


class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="p", attr=attr, content=content, tag_type="double")


class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="div", attr=attr, content=content, tag_type="double")


class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="span", attr=attr, content=content, tag_type="double")


class Hr(Elem):
    def __init__(self, attr={}):
        super().__init__(tag="hr", attr=attr, content=None, tag_type="simple")


class Br(Elem):
    def __init__(self, attr={}):
        super().__init__(tag="br", attr=attr, content=None, tag_type="simple")


def main():
    """Demonstrate all HTML element classes defined in elements.py"""

    # === 1. Html, Head, Body, Title - Basic document structure ===
    print("=" * 60)
    print("1. Html, Head, Body, Title - Basic document structure")
    print("=" * 60)
    doc = Html([Head(Title(Text("My Page Title"))), Body()])
    print(doc)

    # === 2. Meta - Metadata element (simple/self-closing tag) ===
    print("\n" + "=" * 60)
    print("2. Meta - Metadata element (self-closing tag)")
    print("=" * 60)
    head_with_meta = Head(
        [
            Meta({"charset": "UTF-8"}),
            Meta({"name": "viewport", "content": "width=device-width"}),
            Title(Text("Page with Meta")),
        ]
    )
    print(head_with_meta)

    # === 3. H1, H2 - Heading elements ===
    print("\n" + "=" * 60)
    print("3. H1, H2 - Heading elements")
    print("=" * 60)
    headings = Div([H1(Text("Main Heading")), H2(Text("Sub Heading"))])
    print(headings)

    # === 4. P - Paragraph element ===
    print("\n" + "=" * 60)
    print("4. P - Paragraph element")
    print("=" * 60)
    paragraph = P(Text("This is a paragraph with some text content."))
    print(paragraph)

    # === 5. Div, Span - Container elements ===
    print("\n" + "=" * 60)
    print("5. Div, Span - Container elements")
    print("=" * 60)
    containers = Div(
        [
            Span(Text("Inline text in span"), {"class": "highlight"}),
            Div(Text("Block content in div"), {"id": "content-box"}),
        ],
        {"class": "container"},
    )
    print(containers)

    # === 6. Img - Image element (self-closing tag) ===
    print("\n" + "=" * 60)
    print("6. Img - Image element (self-closing tag)")
    print("=" * 60)
    image = Img({"src": "photo.jpg", "alt": "A beautiful photo"})
    print(image)

    # === 7. Ul, Li - Unordered list ===
    print("\n" + "=" * 60)
    print("7. Ul, Li - Unordered list")
    print("=" * 60)
    unordered_list = Ul(
        [Li(Text("First item")), Li(Text("Second item")), Li(Text("Third item"))]
    )
    print(unordered_list)

    # === 8. Ol, Li - Ordered list ===
    print("\n" + "=" * 60)
    print("8. Ol, Li - Ordered list")
    print("=" * 60)
    ordered_list = Ol(
        [Li(Text("Step one")), Li(Text("Step two")), Li(Text("Step three"))]
    )
    print(ordered_list)

    # === 9. Table, Tr, Th, Td - Table elements ===
    print("\n" + "=" * 60)
    print("9. Table, Tr, Th, Td - Table elements")
    print("=" * 60)
    table = Table(
        [
            Tr([Th(Text("Name")), Th(Text("Age")), Th(Text("City"))]),
            Tr([Td(Text("Alice")), Td(Text("30")), Td(Text("Paris"))]),
            Tr([Td(Text("Bob")), Td(Text("25")), Td(Text("London"))]),
        ],
        {"border": "1"},
    )
    print(table)

    # === 10. Hr - Horizontal rule (self-closing tag) ===
    print("\n" + "=" * 60)
    print("10. Hr - Horizontal rule (self-closing tag)")
    print("=" * 60)
    print(Hr())

    # === 11. Br - Line break (self-closing tag) ===
    print("\n" + "=" * 60)
    print("11. Br - Line break (self-closing tag)")
    print("=" * 60)
    text_with_break = P([Text("Line one"), Br(), Text("Line two")])
    print(text_with_break)

    # === 12. Complete page example using ALL elements ===
    print("\n" + "=" * 60)
    print("12. Complete HTML page using ALL element classes")
    print("=" * 60)
    full_page = Html(
        [
            Head([Meta({"charset": "UTF-8"}), Title(Text("Complete Demo Page"))]),
            Body(
                [
                    Div(
                        [
                            H1(Text("Welcome to My Website")),
                            H2(Text("About Us")),
                            P(Text("We are a company that does amazing things.")),
                            Hr(),
                            H2(Text("Our Team")),
                            Table(
                                [
                                    Tr([Th(Text("Name")), Th(Text("Role"))]),
                                    Tr([Td(Text("Alice")), Td(Text("Developer"))]),
                                    Tr([Td(Text("Bob")), Td(Text("Designer"))]),
                                ]
                            ),
                            Hr(),
                            H2(Text("Services")),
                            Ul(
                                [
                                    Li(Text("Web Development")),
                                    Li(Text("Mobile Apps")),
                                    Li(Text("Consulting")),
                                ]
                            ),
                            H2(Text("Process")),
                            Ol(
                                [
                                    Li(Text("Discovery")),
                                    Li(Text("Design")),
                                    Li(Text("Development")),
                                    Li(Text("Delivery")),
                                ]
                            ),
                            Div(
                                [
                                    P(
                                        [
                                            Text("Contact us at "),
                                            Span(
                                                Text("info@example.com"),
                                                {"class": "email"},
                                            ),
                                        ]
                                    ),
                                    Img({"src": "logo.png", "alt": "Company Logo"}),
                                    Br(),
                                    Text("Thank you for visiting!"),
                                ],
                                {"class": "footer"},
                            ),
                        ],
                        {"class": "main-container"},
                    )
                ]
            ),
        ]
    )
    print(full_page)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
