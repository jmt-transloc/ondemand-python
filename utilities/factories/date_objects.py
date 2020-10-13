from datetime import datetime, timedelta


def build_date_string(days=0, hours=0) -> str:
    """Create a new string version of a datetime object for OnDemand testing.

    :param days: The number of days in the past or future from today.
    :param hours: The number of hours in the past or future from this moment.
    """
    return (datetime.utcnow() + timedelta(days=days, hours=hours)).strftime(
        '%Y-%m-%dT%H:%M:%S.000Z',
    )
