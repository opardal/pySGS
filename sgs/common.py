"""
Shared functions.
"""
from datetime import datetime
import locale
from typing import Union
import os


LRU_CACHE_SIZE = 32
MAX_ATTEMPT_NUMBER = 5


def to_datetime(date_string: str, language: str) -> str:
    """ Converts a date string to a datetime object """
    locales = {"pt": "pt_BR.utf-8", "en": "en_US.utf-8"}

    """ correct problem with locale in Windows platform """
    if os.name == 'nt':
        locales = {"pt": "Portuguese_Brazil.1252", "en": "Portuguese_Brazil.1252"}
    
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
        date = date_string
        #raise TypeError("Please, use 'DD/MM/YYYY', 'MMM/YYYY'  or 'YYYY' format for date strings.")
    return date

