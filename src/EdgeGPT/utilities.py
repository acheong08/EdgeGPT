import json
import locale
import random
from typing import Union

from .constants import DELIMITER
from .locale import LocationHint


def append_identifier(msg: dict) -> str:
    # Convert dict to json string
    return json.dumps(msg, ensure_ascii=False) + DELIMITER


def get_ran_hex(length: int = 32) -> str:
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def get_location_hint_from_locale(locale: str) -> Union[dict, None]:
    locale = locale.lower()
    if locale == "en-us":
        hint = LocationHint.USA.value
    elif locale == "zh-cn":
        hint = LocationHint.CHINA.value
    elif locale == "en-gb":
        hint = LocationHint.UK.value
    elif locale == "en-ie":
        hint = LocationHint.EU.value
    else:
        hint = LocationHint.USA.value
    return hint.get("LocationHint")


def guess_locale() -> str:
    loc, _ = locale.getlocale()
    if not loc or len(loc) > 5:
        loc = "en-US"
    return loc.replace("_", "-")
