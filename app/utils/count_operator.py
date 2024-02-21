import os

file_path = "count.txt"


def increase_counter():
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("1")
            return

    with open(file_path, 'r') as file:
        number = int(file.read())

    number += 1

    with open(file_path, 'w') as file:
        file.write(str(number))
