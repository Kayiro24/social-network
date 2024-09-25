import random
import string


def generate_username():
    characters = string.ascii_letters + string.digits
    username_length = 12

    username = ''.join(random.choice(characters) for _ in range(username_length))

    return username
