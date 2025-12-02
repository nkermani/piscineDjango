#!/usr/bin/env python3

import sys


def get_state(capital_city):
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver",
    }

    for abbr, city in capital_cities.items():
        if city == capital_city:
            for state, state_abbr in states.items():
                if state_abbr == abbr:
                    return state
    return None


def main():
    if len(sys.argv) != 2:
        exit()
    capital_city = sys.argv[1]
    state = get_state(capital_city)
    if state:
        print(f"{state}")
    else:
        print("Unknown capital city")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Error")
        exit()
