import random

def generate_number_plate():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"

    plate = (
        random.choice(letters) +
        random.choice(letters) +
        str(random.randint(10,99)) +
        random.choice(letters) +
        random.choice(letters) +
        str(random.randint(1000,9999))
    )

    return plate