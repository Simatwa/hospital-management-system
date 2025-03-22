"""Utilities fuctions for v1
"""

import uuid
import random
from string import ascii_lowercase
from datetime import datetime

token_id = "pms_"


def generate_token() -> str:
    """Generates api token"""
    return token_id + str(uuid.uuid4()).replace("-", random.choice(ascii_lowercase))


def get_day_and_shift(time: datetime) -> tuple[str]:
    day_of_week: str = time.strftime("%A")
    work_shift: str = "Day" if 6 <= time.hour < 18 else "Night"
    return day_of_week, work_shift
