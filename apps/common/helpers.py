from random import choices
from string import ascii_letters
from string import digits

import stripe

from config import settings

stripe.api_key = settings.STRIPE_SECRET_TEST_API_KEY


def decimal_to_int_stripe(money):
    """
    Used to format decimal price for charge.
    """
    return int(money * 100)


def generate_code() -> str:
    """Generate a random  code"""
    code_len = 6
    char_set = ascii_letters + digits
    code = "".join(choices(char_set, k=code_len))
    return code
