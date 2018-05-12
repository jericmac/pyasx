

import dateutil.parser


class UnknownTickerException(Exception):
    """
    Exception thrown when a lookup failed because the ticker doesn't match a
    company/security.
    """

    pass


class LookupError(Exception):
    """
    Exception thrown when there is an error while doing a looking up on
    ASX.com.au
    """

    pass


def _parse_datetime(datetime_string):
    """
    Parse a date time string, in the format used by ASX.com.au
    :return: Parsed datetime object if valid, None if invalid date
    """

    datetime_parsed = None

    try:

        if datetime_string is not None and len(datetime_string):
            datetime_parsed = dateutil.parser.parse(str(datetime_string))

    except ValueError:
        # date parse failed

        datetime_parsed = None

    return datetime_parsed


def _format_date(datetime_obj):
    """
    Format datetime to same format as used on ASX.com.au
    """

    datetime_string = ''

    if datetime_obj is not None:
        datetime_string = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S%z')

    return datetime_string
