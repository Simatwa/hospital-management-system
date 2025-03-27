"""Utilities fuctions for v1
"""

import uuid
import random
from string import ascii_lowercase
from datetime import datetime

import markdown

token_id = "pms_"

markdown_extensions = [
    "markdown.extensions.abbr",
    "markdown.extensions.admonition",
    "markdown.extensions.attr_list",
    # "markdown.extensions.codehilite",
    "markdown.extensions.def_list",
    "markdown.extensions.extra",
    "markdown.extensions.fenced_code",
    "markdown.extensions.footnotes",
    "markdown.extensions.legacy_attrs",
    "markdown.extensions.legacy_em",
    "markdown.extensions.meta",
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists",
    "markdown.extensions.tables",
    "markdown.extensions.toc",
]


def generate_token() -> str:
    """Generates api token"""
    return token_id + str(uuid.uuid4()).replace("-", random.choice(ascii_lowercase))


def get_day_and_shift(time: datetime) -> tuple[str]:
    day_of_week: str = time.strftime("%A")
    work_shift: str = "Day" if 6 <= time.hour < 18 else "Night"
    return day_of_week, work_shift


def markdown_to_html(content: str) -> str:
    return markdown.markdown(text=content, extensions=markdown_extensions)
