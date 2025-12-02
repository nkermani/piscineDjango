#!  /usr/bin/env python3

import random
import beverages


class CoffeeMachine:

    def __init__(self):
        self.serve_count = 0

    class EmptyCup(beverages.HotBeverage):
        name = "empty cup"
        price = 0.90

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def repair(self):
        self.serve_count = 0

    def serve(self, beverage_class):
        if self.serve_count >= 10:
            raise self.BrokenMachineException()

        self.serve_count += 1

        if random.randint(0, 1) == 0:
            return beverage_class()
        else:
            return self.EmptyCup()


def main():
    machine = CoffeeMachine()
    beverages_list = [
        beverages.Coffee,
        beverages.Tea,
        beverages.Chocolate,
        beverages.Cappuccino,
    ]

    for _ in range(15):
        try:
            beverage_class = random.choice(beverages_list)
            beverage = machine.serve(beverage_class)
            print(beverage)
        except CoffeeMachine.BrokenMachineException as e:
            print(e)

    machine.repair()

    for _ in range(15):
        try:
            beverage_class = random.choice(beverages_list)
            beverage = machine.serve(beverage_class)
            print(beverage)
        except CoffeeMachine.BrokenMachineException as e:
            print(e)


if __name__ == "__main__":
    main()
