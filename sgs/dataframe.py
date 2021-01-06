"""
Dataframe
"""
from typing import Dict, List, Tuple, Union, Optional

import pandas as pd

from . import api
from . import search
from .ts import time_serie
from .common import get_series_codes


def dataframe(ts_codes: Union[int, List, Tuple], start: str, end: Optional[str] = None, strict: bool = False) -> pd.DataFrame:
    """
    Creates a dataframe from a list of time serie codes.

    :param ts_codes: single code or list/tuple of time series codes.
    :param start: start date (DD/MM/YYYY).
    :param end: end date (DD/MM/YYYY).
    :param strict: boolean to enforce a strict date range.

    :return: Pandas dataframe.
    :rtype: pandas.DataFrame_

    Usage::

        >>> CDI = 12
        >>> INCC = 192  #  National Index of Building Costs
        >>> df = sgs.dataframe([CDI, INCC], start='02/01/2018', end='31/12/2018')
        >>> df.head()
                         12    192
        2018-01-01       NaN  0.31
        2018-01-02  0.026444   NaN
        2018-01-03  0.026444   NaN
        2018-01-04  0.026444   NaN
        2018-01-05  0.026444   NaN

    """

    series = []
    for code in get_series_codes(ts_codes):
        ts = time_serie(code, start, end, strict)
        series.append(ts)

    df = pd.concat(series, axis=1)
    return df
