def my_numbers():
    with open("numbers.txt", "r") as file:
        content = file.read().strip()
        numbers = content.split(",")
        for number in numbers:
            print(number)


if __name__ == "__main__":
    my_numbers()
