#!/usr/bin/env python3


def parse_element(line):
    name, data = line.strip().split(" = ")
    attributes = {}
    for item in data.split(", "):
        key, value = item.split(":")
        attributes[key.strip()] = value.strip()
    return name, attributes


def read_periodic_table(filename):
    try:
        elements = []
        with open(filename, "r") as f:
            for line in f:
                if line.strip():
                    name, attributes = parse_element(line)
                    elements.append(
                        {
                            "name": name,
                            "position": int(attributes["position"]),
                            "number": int(attributes["number"]),
                            "symbol": attributes["small"],
                            "molar": attributes["molar"],
                            "electron": attributes["electron"],
                        }
                    )
        return elements
    except Exception:
        print("Can't open periodic_table.txt file.")
        exit()


def get_element_color(number):
    if number in [2, 10, 18, 36, 54, 86, 118]:
        return "#c0ffff"
    elif number in [3, 11, 19, 37, 55, 87]:
        return "#ff6666"
    elif number in [4, 12, 20, 38, 56, 88]:
        return "#ffdead"
    elif number in range(57, 72):
        return "#ffbfff"
    elif number in range(89, 104):
        return "#ff99cc"
    elif number in [
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
    ]:
        return "#ffc0c0"
    elif number in [13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116]:
        return "#cccccc"
    elif number in [5, 14, 32, 33, 51, 52, 85]:
        return "#cccc99"
    elif number in [1, 6, 7, 8, 15, 16, 34]:
        return "#a0ffa0"
    elif number in [9, 17, 35, 53, 117]:
        return "#ffff99"
    else:
        return "#ffffff"


def generate_html(elements):
    elements_sorted = sorted(elements, key=lambda x: x["number"])
    rows = []
    current_row = []

    for element in elements_sorted:
        current_row.append(element)
        if element["number"] in [2, 10, 18, 36, 54, 86, 118]:
            rows.append(current_row)
            current_row = []

    if current_row:
        rows.append(current_row)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Periodic Table</title>
    <link rel="stylesheet" href="periodic_table.css">
</head>
<body>
    <table>
"""

    for row in rows:
        html += "        <tr>\n"
        row_sorted = sorted(row, key=lambda x: x["position"])
        current_position = 0
        added_gap = False

        for element in row_sorted:
            while current_position < element["position"]:
                html += '            <td class="empty"></td>\n'
                current_position += 1

            if element["position"] >= 3 and not added_gap:
                html += '            <td class="empty"></td>\n'
                added_gap = True

            bg_color = get_element_color(element["number"])
            html += f'            <td style="background-color: {bg_color};">\n'
            html += f'                <h4>{element["name"]}</h4>\n'
            html += f"                <ul>\n"
            html += f'                    <li>Number: {element["number"]}</li>\n'
            html += f'                    <li>Symbol: {element["symbol"]}</li>\n'
            html += f'                    <li>Atomic mass: {element["molar"]}</li>\n'
            html += f"                </ul>\n"
            html += f"            </td>\n"
            current_position += 1

        total_cols = 19
        while current_position < total_cols:
            html += '            <td class="empty"></td>\n'
            current_position += 1

        html += "        </tr>\n"

    html += """    </table>
</body>
</html>"""

    return html


def generate_css():
    css = """body {
    font-family: Arial, sans-serif;
    padding: 20px;
}

table {
    border-collapse: collapse;
    border-spacing: 0;
}

td {
    border: 1px solid #333;
    width: 100px;
    height: 100px;
    padding: 5px;
    vertical-align: top;
    text-align: left;
}

td.empty {
    border: none;
}

h4 {
    margin: 0 0 5px 0;
    font-size: 14px;
    text-align: center;
}

ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    font-size: 11px;
}

li {
    margin: 3px 0;
}
"""
    return css


def main():
    elements = read_periodic_table("periodic_table.txt")
    html = generate_html(elements)
    css = generate_css()

    with open("periodic_table.html", "w") as f:
        f.write(html)

    with open("periodic_table.css", "w") as f:
        f.write(css)

    print("periodic_table.html has been generated successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Error")
        exit()
