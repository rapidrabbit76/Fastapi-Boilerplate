import typing as T
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from pandas.tseries.offsets import Week


class DateUnit(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


def build_resample_rule(date_unit: DateUnit):
    if date_unit is DateUnit.DAY:
        rule = "1D"
    elif date_unit is DateUnit.WEEK:
        rule = Week(weekday=6)
        # rule = "7D"
    elif date_unit is DateUnit.MONTH:
        rule = "MS"
    return rule
