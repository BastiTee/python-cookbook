r"""This module contains date/time conversion tools.

References for format strings:
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
"""

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import time

DEFAULT_CONVERT_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DEFAULT_CONVERT_FORMAT_BOD = '%Y-%m-%d 00:00:00.000'
DEFAULT_CONVERT_FORMAT_EOD = '%Y-%m-%d 23:59:59.999'


def validate_input(input):
    if input is None:
        raise ValueError('None-input is not allowed.')


def epoch_to_timestamp(epoch, formatstring=DEFAULT_CONVERT_FORMAT):
    """Converts an epoch to a human-readable timestamp."""

    validate_input(epoch)
    epoch = float(epoch)
    return dto_to_timestamp(epoch_to_dto(epoch), formatstring)


def epoch_to_dto(epoch):
    """Converts an epoch to a python datetime object."""

    validate_input(epoch)
    epoch = float(epoch)
    return (datetime.fromtimestamp(epoch) +
            timedelta(seconds=time.timezone))


def timestamp_to_dto(timestamp, formatstring=DEFAULT_CONVERT_FORMAT):
    """"Converts a human-readable timestamp to a python datetime object."""

    validate_input(timestamp)
    return datetime.strptime(timestamp, formatstring)


def timestamp_to_epoch(timestamp, formatstring=DEFAULT_CONVERT_FORMAT):
    """Converts a human-readable timestamp to an epoch."""

    validate_input(timestamp)
    return dto_to_epoch(timestamp_to_dto(timestamp, formatstring))


def dto_to_timestamp(dto, formatstring=DEFAULT_CONVERT_FORMAT):
    """Converts a python datetime object to a human-readable timestamp."""

    validate_input(dto)
    return dto.strftime(formatstring)


def dto_to_epoch(dto):
    """Converts a python datetime object to an epoch."""

    validate_input(dto)
    return int(dto.strftime('%s'))


def get_current_datetime_for_filename():
    """Returns a date & time timestamp that can be used for filenames"""

    return datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')


def get_current_date_for_filename():
    """Returns a date timestamp that can be used for filenames"""

    return datetime.fromtimestamp(time.time()).strftime('%Y%m%d')


def get_intervals(start_epoch, end_epoch, interval='week',
                  output_format=DEFAULT_CONVERT_FORMAT):
    """Return a list of tuples representing the intervals between the
    two given epoch timestamps."""
    def get_interval_sec(interval):
        return {
            'week': relativedelta(weeks=+1),
            'day': relativedelta(days=+1)
        }.get(interval, None)
    interval_sec = get_interval_sec(interval)
    if not interval_sec:
        raise ValueError('Unsupported interval \'{}\'. '.format(interval) +
                         'Allowed values: week, day')
    start = epoch_to_dto(start_epoch)
    end = epoch_to_dto(end_epoch)
    start_iv = start
    intervals = []
    while True:
        end_iv = start_iv + interval_sec
        # start_iv_shift = epoch_to_dto(dto_to_epoch(start_iv) + 1)
        siv = dto_to_timestamp(
            start_iv + timedelta(seconds=1), output_format)
        eiv = dto_to_timestamp(end_iv, output_format)
        # print('{} {}'.format(siv, eiv))
        intervals.append((siv, eiv))
        if end_iv >= end:
            return intervals
        start_iv = end_iv


def now():
    """Return the current time as date object."""
    return datetime.now()


def now_epoch():
    """Return the current time as epoch."""
    return dto_to_epoch(now())


def get_start_end_of_today():
    """Return the start/end unix timestamp and str ts for current day."""
    today = date.today()
    begintime = today.strftime(DEFAULT_CONVERT_FORMAT_BOD)
    endtime = today.strftime(DEFAULT_CONVERT_FORMAT_EOD)
    begintime_epoch = timestamp_to_epoch(begintime)
    endtime_epoch = timestamp_to_epoch(endtime)

    return (begintime, endtime, begintime_epoch, endtime_epoch)


def get_epoch_center_from_timestamps(
        date_a, date_b, formatstring=DEFAULT_CONVERT_FORMAT):
    """Return the date with identical distance between the two given dates."""
    ep_a = timestamp_to_epoch(date_a, formatstring)
    ep_b = timestamp_to_epoch(date_b, formatstring)
    ep_left = min(ep_a, ep_b)
    ep_right = max(ep_a, ep_b)
    return ep_left + (ep_right - ep_left) / 2


def get_week_number_from_epoch(epoch):
    """Return week number from epoch."""
    return epoch_to_dto(epoch).isocalendar()[1]
