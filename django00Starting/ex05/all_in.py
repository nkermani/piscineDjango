import sys

states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
capital_cities = {"OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver"}


def normalize_str(element):
    return element.strip().title()


def parsing(str_input):
    if str_input:
        items = str_input.split(",")
        return [normalize_str(item) for item in items]
    return []


def get_state(capital_city):
    capital_city = capital_city.strip()
    for abbr, city in capital_cities.items():
        if city == capital_city:
            for state, state_abbr in states.items():
                if state_abbr == abbr:
                    return state
    return None


def get_capital_city(state):
    state = state.strip()
    state_abbr = states.get(state)
    if state_abbr:
        return capital_cities.get(state_abbr)
    return None


def loop(items):
    for item in items:
        if item == "":
            continue
        state = get_state(item)
        if state:
            print(f"{item} is the capital of {state}")
            continue

        capital = get_capital_city(item)
        if capital:
            print(f"{capital} is the capital of {item}")
            continue
        print(f"{item} is neither a capital city nor a state")
    return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit()
    str_input = sys.argv[1]
    items = parsing(str_input)
    loop(items)
