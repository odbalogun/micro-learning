import random
import string


def random_string(length):
    """
    Creates a random string
    :param length: String length of the string to return
    :return: String
    """
    random_list = []
    for i in range(length):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return ''.join(random_list)
