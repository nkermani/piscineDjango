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


# def main():
#     print("### Testing #1 (from Subject) ###")
#     print(Html([Head(), Body()]))
#     print("\n### Testing #2 (from Subject) ###")
#     print(
#         Html(
#             [
#                 Head(Title(Text("Hello ground!"))),
#                 Body(
#                     [
#                         H1(Text("Oh no, not again!")),
#                         Img({"src": "http://i.imgur.com/pfp3T.jpg"}),
#                     ]
#                 ),
#             ]
#         )
#     )
#     print("\n### Testing #3 ###")
#     table = Table(
#         [
#             Tr([Th(Text("Name")), Th(Text("Age")), Th(Text("City"))]),
#             Tr([Td(Text("Alice")), Td(Text("30")), Td(Text("New York"))]),
#             Tr([Td(Text("Bob")), Td(Text("25")), Td(Text("Los Angeles"))]),
#             Tr([Td(Text("Charlie")), Td(Text("35")), Td(Text("Chicago"))]),
#         ]
#     )
#     print(table)
#     return


# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         print(f"Error: {e}")
