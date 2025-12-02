#!/usr/bin/env python3

import sys


def get_capital_city(state):
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver",
    }

    state_abbr = states.get(state)
    if state_abbr:
        return capital_cities.get(state_abbr)
    return None


def main():
    if len(sys.argv) != 2:
        exit()
    state = sys.argv[1]
    capital = get_capital_city(state)
    if capital:
        print(f"{capital}")
    else:
        print("Unknown state")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Error")
        exit()
