from random import random


def get_random_value(multiplier: int | float) -> float:
    """
    Get a random value multiplied by a given number.
    Args:
        multiplier (int | float): The number to multiply the random value by.
    Returns:
        float: A random value multiplied by the given number.
    """
    return random() * multiplier
