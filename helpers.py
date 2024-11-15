import datetime


def format_timedelta_to_short_string(timedelta_to_format: datetime.timedelta) -> str:
    seconds = timedelta_to_format.seconds

    if seconds < 60:
        return f"{seconds} sec"

    minutes, seconds = divmod(seconds, 60)

    if minutes < 60:
        return f"{minutes}m{seconds}sec"

    hours, minutes = divmod(minutes, 60)

    return f"{hours}h{minutes}m{seconds}s"
