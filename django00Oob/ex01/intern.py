#!/usr/bin/env python3


class Intern:
    # Constructor with default name
    def __init__(self, Name="My name? I’m nobody, an intern, I have no name."):
        self.Name = Name

    def __str__(self):
        return self.Name

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")

    def make_coffee(self):
        return self.Coffee()


def main():
    intern = Intern()
    print(intern)

    mark = Intern("Mark")
    print("My name is:", mark)

    coffee = mark.make_coffee()
    print(coffee)

    try:
        intern.work()
    except Exception as e:
        print(e)  # Print exception message when trying to work


if __name__ == "__main__":
    main()
