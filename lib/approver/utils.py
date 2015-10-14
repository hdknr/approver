import random

try:
    random = random.SystemRandom()
except NotImplementedError:
    pass


def get_random_string(
    length=32,
    allowed_chars='abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  '0123456789'):
        return ''.join([random.choice(allowed_chars) for i in range(length)])
