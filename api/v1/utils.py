"""Utilities fuctions for v1
"""

import uuid
import random
from string import ascii_lowercase

token_id = "pms_"


def generate_token() -> str:
    """Generates api token"""
    return token_id + str(uuid.uuid4()).replace("-", random.choice(ascii_lowercase))
