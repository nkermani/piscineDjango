#!/usr/bin/env python3


def my_numbers():
    try:
        with open("numbers.txt", "r") as file:
            content = file.read().strip()
            numbers = content.split(",")
            for number in numbers:
                print(number)
    except FileNotFoundError:
        print("Le fichier 'numbers.txt' est introuvable.")


def main():
    my_numbers()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Error")
        exit()
