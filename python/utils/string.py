import string
import random


def random_string(n: int=10) -> str:
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

