r"""This module contains date/time conversion tools.
References for format strings:
- https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
"""

from datetime import datetime
from dateutil.relativedelta import *
import time

DEFAULT_CONVERT_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


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
    return datetime.fromtimestamp(epoch)


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


def print_intervals(start_timestamp, end_timestamp,
                    interval_sec=relativedelta(months=+1),
                    input_format=DEFAULT_CONVERT_FORMAT,
                    output_format=DEFAULT_CONVERT_FORMAT,
                    list_format='{} {}'):
    """Print one interval per line for the given time span."""
    start = timestamp_to_dto(start_timestamp, input_format)
    end = timestamp_to_dto(end_timestamp, input_format)
    start_iv = start
    while True:
        end_iv = start_iv + interval_sec
        print(list_format.format(
            dto_to_timestamp(start_iv, output_format),
            dto_to_timestamp(end_iv, output_format)))
        if end_iv >= end:
            break
        start_iv = end_iv


def now():
    """Return the current time as date object."""
    return datetime.now()
