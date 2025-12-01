import sys

states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
capital_cities = {"OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver"}


def get_capital_city(state):
    state_abbr = states.get(state)
    if state_abbr:
        return capital_cities.get(state_abbr)
    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit()
    state = sys.argv[1]
    capital = get_capital_city(state)
    if capital:
        print(f"{capital}")
    else:
        print("Unknown state")
