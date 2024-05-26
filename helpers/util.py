from dateutil.relativedelta import *
from datetime import datetime

window_part_map = {"H": "hours", "D": "days", "W": "weeks", "M": "months", "Y": "years"}


def parse_window(window: str) -> relativedelta:
    """
    Sets the offset based on the window
    :param window: time partition such as "1D"
    :return: upperbound (non-inclusive) of the time partition
    """
    window_num = int(window[:-1])
    window_part = window_part_map.get(window[-1:].upper(),None)
    if window_num <= 0:
        raise Exception("Unsupported time increment. Must be greater than 0")
    if not window_part:
        raise Exception("Unsupported time partition. Must be H, D, W, M, or Y")

    return relativedelta(**{window_part: window_num})


def get_window_start(window: str, dt: datetime) -> datetime:
    """
    Rounds down to the window timeframe.
    For example, if 1M then it will set the day to 1
    If the window is set as "w", will go to the start of the week (ISO Week, so Monday)
    :param window: time partition such as "1D"
    :param dt: the datetime to round
    :return: the rounded down datetime
    """
    round_time_parts = {"microsecond": 0, "second": 0, "minute": 0}
    window_part = window[-1:].lower()

    for time_part in window_part_map.values():
        if time_part.startswith(window_part):
            break

        # weeks is not part of datetime, so skip
        if time_part != "weeks":
            # set the start value to 1
            default_val = 0 if time_part == "hours" else 1
            round_time_parts[time_part.rstrip("s")] = default_val

    # If week, get the beginning of the week
    if window_part == "w":
        dt -= relativedelta(days=dt.weekday())

    return dt.replace(**round_time_parts)

