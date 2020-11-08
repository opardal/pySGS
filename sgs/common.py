"""
Shared functions.
"""
from datetime import datetime
import locale
import os


LRU_CACHE_SIZE = 32
MAX_ATTEMPT_NUMBER = 5


def to_datetime(date_string: str, language: str) -> datetime:

    """ correct problem with locale in Windows platform """
    if os.name == "nt":
        locales = {"pt": "Portuguese_Brazil.1252", "en": "Portuguese_Brazil.1252"}
    else:
        locales = {"pt": "pt_BR.utf-8", "en": "en_US.utf-8"}

    locale.setlocale(locale.LC_TIME, locales[language])

    dd_mm_aaaa = "%d/%m/%Y"
    mmm_aaaa = "%b/%Y"
    aaaa = "%Y"

    formats = [dd_mm_aaaa, mmm_aaaa, aaaa]

    for fmt in formats:
        try:
            date = datetime.strptime(date_string, fmt)
            if fmt == aaaa:
                date = date.replace(day=31, month=12)
            break
        except ValueError:
            continue
    else:
        raise ValueError
    return date


def to_datetime_string(date_string: str, language: str) -> str:

    try:
        date = to_datetime(date_string, language).strftime("%Y-%m-%d")
    except ValueError:
        date = date_string
    return date
