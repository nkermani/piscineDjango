#!/usr/bin/python3

from elements import (
    Html,
    Head,
    Body,
    Title,
    Meta,
    Img,
    Table,
    Th,
    Tr,
    Td,
    Ul,
    Ol,
    Li,
    H1,
    H2,
    P,
    Div,
    Span,
    Hr,
    Br,
)
from elem import Text, Elem


class Page:
    def __init__(self, elem):
        if not isinstance(elem, Elem):
            raise Elem.ValidationError("Page content must be an Elem instance")
        self.elem = elem

    def __str__(self):
        """Return HTML code, with doctype if root element is Html."""
        if isinstance(self.elem, Html):
            return "<!DOCTYPE html>\n" + str(self.elem)
        return str(self.elem)

    def write_to_file(self, filename):
        """Write HTML code to a file, with doctype if root element is Html."""
        with open(filename, "w") as f:
            f.write(str(self))

    def is_valid(self):
        return self._validate_elem(self.elem)

    def _validate_elem(self, elem):
        if isinstance(elem, Text):
            return True

        if not isinstance(elem, Elem):
            return False

        if isinstance(elem, Html):
            if not self._validate_html(elem):
                return False
        elif isinstance(elem, Head):
            if not self._validate_head(elem):
                return False
        elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
            if not self._validate_single_text(elem):
                return False
        elif isinstance(elem, P):
            if not self._validate_texts_only(elem):
                return False
        elif isinstance(elem, Span):
            if not self._validate_span(elem):
                return False
        elif isinstance(elem, (Ul, Ol)):
            if not self._validate_list(elem):
                return False
        elif isinstance(elem, Tr):
            if not self._validate_tr(elem):
                return False
        elif isinstance(elem, Table):
            if not self._validate_table(elem):
                return False
        elif isinstance(elem, (Body, Div)):
            if not self._validate_body_or_div(elem):
                return False

        for content in elem.content:
            if not self._validate_elem(content):
                return False

        return True

    def _validate_html(self, elem):
        head_count = sum(1 for c in elem.content if isinstance(c, Head))
        body_count = sum(1 for c in elem.content if isinstance(c, Body))
        if head_count != 1 or body_count != 1:
            return False
        # Check order: Head must come before Body
        if len(elem.content) == 2:
            if not isinstance(elem.content[0], Head) or not isinstance(
                elem.content[1], Body
            ):
                return False
        for content in elem.content:
            if not isinstance(content, (Head, Body)):
                return False
        return True

    def _validate_head(self, elem):
        title_count = sum(1 for c in elem.content if isinstance(c, Title))
        if title_count != 1:
            return False
        for content in elem.content:
            if not isinstance(content, (Title, Meta)):
                return False
        return True

    def _validate_single_text(self, elem):
        if len(elem.content) != 1:
            return False
        if not isinstance(elem.content[0], Text):
            return False
        return True

    def _validate_texts_only(self, elem):
        for content in elem.content:
            if not isinstance(content, Text):
                return False
        return True

    def _validate_span(self, elem):
        for content in elem.content:
            if not isinstance(content, (Text, P)):
                return False
        return True

    def _validate_list(self, elem):
        if len(elem.content) == 0:
            return False
        for content in elem.content:
            if not isinstance(content, Li):
                return False
        return True

    def _validate_tr(self, elem):
        if len(elem.content) == 0:
            return False
        has_th = any(isinstance(c, Th) for c in elem.content)
        has_td = any(isinstance(c, Td) for c in elem.content)
        if not (has_th or has_td):
            return False
        if has_th and has_td:
            return False
        for content in elem.content:
            if not isinstance(content, (Th, Td)):
                return False
        return True

    def _validate_table(self, elem):
        for content in elem.content:
            if not isinstance(content, Tr):
                return False
        return True

    def _validate_body_or_div(self, elem):
        for content in elem.content:
            if not isinstance(
                content, (H1, H2, Div, Table, Ul, Ol, Span, Text, P, Hr, Br, Img)
            ):
                return False
        return True


########################################################################################################
####################################### MAIN ###########################################################
########################################################################################################


def main():
    def test(description, elem, expected):
        """Helper to run a test and display result"""
        page = Page(elem)
        result = page.is_valid()
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status} | Expected: {expected}, Got: {result} | {description}")
        return result == expected

    print("=" * 70)
    print("PAGE VALIDATION TEST SUITE")
    print("=" * 70)

    # ========== HTML VALIDATION ==========
    print("\n### 1. Html validation (must have exactly 1 Head and 1 Body) ###\n")

    # TRUE: Valid Html with Head and Body
    test("Html with 1 Head + 1 Body", Html([Head(Title(Text("T"))), Body()]), True)

    # FALSE: Html with no Head
    test("Html with 0 Head + 1 Body", Html([Body()]), False)

    # FALSE: Html with no Body
    test("Html with 1 Head + 0 Body", Html([Head(Title(Text("T")))]), False)

    # FALSE: Html with 2 Heads
    test(
        "Html with 2 Heads + 1 Body",
        Html([Head(Title(Text("T"))), Head(Title(Text("T2"))), Body()]),
        False,
    )

    # FALSE: Html with 2 Bodies
    test(
        "Html with 1 Head + 2 Bodies",
        Html([Head(Title(Text("T"))), Body(), Body()]),
        False,
    )

    # FALSE: Html with invalid child (Div instead of Head/Body)
    test(
        "Html with Div child (invalid)",
        Html([Head(Title(Text("T"))), Body(), Div()]),
        False,
    )

    # FALSE: Html with Body before Head (wrong order)
    test(
        "Html with Body before Head (wrong order)",
        Html([Body(), Head(Title(Text("T")))]),
        False,
    )

    # ========== HEAD VALIDATION ==========
    print(
        "\n### 2. Head validation (must have exactly 1 Title, only Title/Meta allowed) ###\n"
    )

    # TRUE: Valid Head with Title only
    test("Head with 1 Title", Html([Head(Title(Text("T"))), Body()]), True)

    # TRUE: Head with Title and Meta
    test(
        "Head with Title + Meta",
        Html([Head([Title(Text("T")), Meta({"charset": "UTF-8"})]), Body()]),
        True,
    )

    # FALSE: Head with no Title
    test("Head with 0 Title", Html([Head(Meta({"charset": "UTF-8"})), Body()]), False)

    # FALSE: Head with 2 Titles
    test(
        "Head with 2 Titles",
        Html([Head([Title(Text("T1")), Title(Text("T2"))]), Body()]),
        False,
    )

    # FALSE: Head with invalid child (H1)
    test(
        "Head with H1 child (invalid)",
        Html([Head([Title(Text("T")), H1(Text("Bad"))]), Body()]),
        False,
    )

    # ========== TITLE, H1, H2, Li, Th, Td VALIDATION ==========
    print(
        "\n### 3. Title/H1/H2/Li/Th/Td validation (must have exactly 1 Text child) ###\n"
    )

    # TRUE: Title with single Text
    test("Title with 1 Text", Html([Head(Title(Text("Valid"))), Body()]), True)

    # FALSE: Title with 2 Text children
    test(
        "Title with 2 Text children",
        Html([Head(Title([Text("A"), Text("B")])), Body()]),
        False,
    )

    # FALSE: Title with no children
    test("Title with 0 children", Html([Head(Title()), Body()]), False)

    # TRUE: H1 with single Text
    test(
        "H1 with 1 Text",
        Html([Head(Title(Text("T"))), Body(H1(Text("Heading")))]),
        True,
    )

    # FALSE: H1 with Span child (not Text)
    test(
        "H1 with Span child (invalid)",
        Html([Head(Title(Text("T"))), Body(H1(Span(Text("Bad"))))]),
        False,
    )

    # TRUE: Li with single Text
    test(
        "Li with 1 Text (in Ul)",
        Html([Head(Title(Text("T"))), Body(Ul(Li(Text("Item"))))]),
        True,
    )

    # ========== P VALIDATION ==========
    print("\n### 4. P validation (can contain only Text children) ###\n")

    # TRUE: P with single Text
    test(
        "P with 1 Text",
        Html([Head(Title(Text("T"))), Body(P(Text("Paragraph")))]),
        True,
    )

    # TRUE: P with multiple Text children
    test(
        "P with multiple Text children",
        Html([Head(Title(Text("T"))), Body(P([Text("A"), Text("B")]))]),
        True,
    )

    # FALSE: P with Span child
    test(
        "P with Span child (invalid)",
        Html([Head(Title(Text("T"))), Body(P(Span(Text("Bad"))))]),
        False,
    )

    # TRUE: P with no children (empty is valid - only Text allowed)
    test("P with 0 children (empty)", Html([Head(Title(Text("T"))), Body(P())]), True)

    # ========== SPAN VALIDATION ==========
    print("\n### 5. Span validation (can contain Text or P only) ###\n")

    # TRUE: Span with Text
    test(
        "Span with Text",
        Html([Head(Title(Text("T"))), Body(Span(Text("Inline")))]),
        True,
    )

    # TRUE: Span with P
    test(
        "Span with P", Html([Head(Title(Text("T"))), Body(Span(P(Text("Para"))))]), True
    )

    # TRUE: Span with multiple Text and P
    test(
        "Span with Text + P",
        Html([Head(Title(Text("T"))), Body(Span([Text("A"), P(Text("B"))]))]),
        True,
    )

    # FALSE: Span with Div child
    test(
        "Span with Div child (invalid)",
        Html([Head(Title(Text("T"))), Body(Span(Div()))]),
        False,
    )

    # ========== UL/OL VALIDATION ==========
    print("\n### 6. Ul/Ol validation (must have >0 children, only Li allowed) ###\n")

    # TRUE: Ul with Li children
    test(
        "Ul with Li children",
        Html([Head(Title(Text("T"))), Body(Ul([Li(Text("A")), Li(Text("B"))]))]),
        True,
    )

    # TRUE: Ol with Li children
    test(
        "Ol with Li children",
        Html([Head(Title(Text("T"))), Body(Ol([Li(Text("1")), Li(Text("2"))]))]),
        True,
    )

    # FALSE: Ul with no children
    test(
        "Ul with 0 children (empty)", Html([Head(Title(Text("T"))), Body(Ul())]), False
    )

    # FALSE: Ol with no children
    test(
        "Ol with 0 children (empty)", Html([Head(Title(Text("T"))), Body(Ol())]), False
    )

    # FALSE: Ul with non-Li child
    test(
        "Ul with P child (invalid)",
        Html([Head(Title(Text("T"))), Body(Ul(P(Text("Bad"))))]),
        False,
    )

    # ========== TR VALIDATION ==========
    print(
        "\n### 7. Tr validation (must have >0 children, only Th OR only Td, not mixed) ###\n"
    )

    # TRUE: Tr with Th only
    test(
        "Tr with Th only",
        Html(
            [Head(Title(Text("T"))), Body(Table(Tr([Th(Text("H1")), Th(Text("H2"))])))]
        ),
        True,
    )

    # TRUE: Tr with Td only
    test(
        "Tr with Td only",
        Html(
            [Head(Title(Text("T"))), Body(Table(Tr([Td(Text("D1")), Td(Text("D2"))])))]
        ),
        True,
    )

    # FALSE: Tr with mixed Th and Td
    test(
        "Tr with Th + Td mixed (invalid)",
        Html([Head(Title(Text("T"))), Body(Table(Tr([Th(Text("H")), Td(Text("D"))])))]),
        False,
    )

    # FALSE: Tr with no children
    test(
        "Tr with 0 children (empty)",
        Html([Head(Title(Text("T"))), Body(Table(Tr()))]),
        False,
    )

    # FALSE: Tr with invalid child (P)
    test(
        "Tr with P child (invalid)",
        Html([Head(Title(Text("T"))), Body(Table(Tr(P(Text("Bad")))))]),
        False,
    )

    # ========== TABLE VALIDATION ==========
    print("\n### 8. Table validation (can only contain Tr children) ###\n")

    # TRUE: Table with Tr children
    test(
        "Table with Tr children",
        Html(
            [
                Head(Title(Text("T"))),
                Body(
                    Table(
                        [
                            Tr([Th(Text("Name")), Th(Text("Age"))]),
                            Tr([Td(Text("Alice")), Td(Text("30"))]),
                        ]
                    )
                ),
            ]
        ),
        True,
    )

    # FALSE: Table with non-Tr child
    test(
        "Table with P child (invalid)",
        Html([Head(Title(Text("T"))), Body(Table(P(Text("Bad"))))]),
        False,
    )

    # TRUE: Empty Table (no children)
    test(
        "Table with 0 children (empty)",
        Html([Head(Title(Text("T"))), Body(Table())]),
        True,
    )

    # ========== BODY/DIV VALIDATION ==========
    print(
        "\n### 9. Body/Div validation (allowed: H1,H2,Div,Table,Ul,Ol,Span,Text,P,Hr,Br,Img) ###\n"
    )

    # TRUE: Body with all valid children
    test(
        "Body with H1, P, Ul",
        Html(
            [
                Head(Title(Text("T"))),
                Body([H1(Text("Heading")), P(Text("Para")), Ul([Li(Text("Item"))])]),
            ]
        ),
        True,
    )

    # TRUE: Body with Hr and Br
    test(
        "Body with Hr and Br", Html([Head(Title(Text("T"))), Body([Hr(), Br()])]), True
    )

    # TRUE: Body with Img
    test(
        "Body with Img",
        Html([Head(Title(Text("T"))), Body(Img({"src": "img.jpg"}))]),
        True,
    )

    # TRUE: Body with nested Div
    test(
        "Body with nested Div",
        Html([Head(Title(Text("T"))), Body(Div(P(Text("Nested"))))]),
        True,
    )

    # FALSE: Body with Title (not allowed in Body)
    test(
        "Body with Title child (invalid)",
        Html([Head(Title(Text("T"))), Body(Title(Text("Bad")))]),
        False,
    )

    # FALSE: Body with Meta (not allowed in Body)
    test(
        "Body with Meta child (invalid)",
        Html([Head(Title(Text("T"))), Body(Meta({"name": "bad"}))]),
        False,
    )

    # ========== COMPLETE VALID PAGE ==========
    print("\n### 10. Complete valid page example ###\n")

    complete_page = Html(
        [
            Head([Title(Text("Complete Test Page")), Meta({"charset": "UTF-8"})]),
            Body(
                [
                    H1(Text("Main Title")),
                    H2(Text("Subtitle")),
                    P(Text("A paragraph with text.")),
                    Hr(),
                    Div(
                        [
                            Span([Text("Some "), P(Text("inline"))]),
                            Ul([Li(Text("Item 1")), Li(Text("Item 2"))]),
                            Ol([Li(Text("Step 1")), Li(Text("Step 2"))]),
                            Table(
                                [
                                    Tr([Th(Text("Col 1")), Th(Text("Col 2"))]),
                                    Tr([Td(Text("A")), Td(Text("B"))]),
                                    Tr([Td(Text("C")), Td(Text("D"))]),
                                ]
                            ),
                            Img({"src": "photo.jpg", "alt": "Photo"}),
                            Br(),
                        ]
                    ),
                ]
            ),
        ]
    )

    test("Complete valid HTML page", complete_page, True)

    # Print the complete page
    print("\n### Complete page HTML output: ###\n")
    print(Page(complete_page))

    print("\n" + "=" * 70)
    print("END OF TESTS")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
