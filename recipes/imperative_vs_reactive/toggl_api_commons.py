#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common functionality for accessing the Toggl API."""

from json import dump, load, loads

from requests import Session


class TogglApiClientDefault():
    """Default real-world Toggl API client.

    Make sure to get an API token and your workspace ID from Toggl first.
    You need to copy the credentials.json.default file to credentials.json
    and replace the values with your actual Toggl credentials.
    """

    def __init__(self, credentials):
        self.credentials = credentials

    def get_working_hours_for_range(self, range_from, range_to):
        """This is the main API call, that fetches the total working hours
        in milliseconds for the given from/to range.
        """
        toggl_api = 'https://toggl.com/reports/api/v2/details'

        # Setup a session with Basic Authentication
        session = Session()
        session.auth = (self.credentials['api_token'], 'api_token')

        # Create request URL
        url = ('{}?workspace_id={}&since={}&until={}&user_agent={}'
               .format(toggl_api, self.credentials['ws_id'], range_from,
                       range_to, self.credentials['user_agent']))

        # Run query
        response = session.get(url)

        # Evaluate result
        if response.status_code != 200:
            raise Exception(
                '[API-REQ] WARN: API request failed ({}) for {}>{}'
                .format(response.status_code, range_from, range_to))

        # If a numeric total grand was found, return it. Otherwise
        # return 0 to indicate, that we weren't working in that period.
        return (loads(response.text)['total_grand']
                if loads(response.text)['total_grand'] else 0)


def create_input_ranges(from_date, to_date):
    """Take the given from-date and to-date and create daily time intervals.

    So the input from_date=2018-03-02 to_date=2018-03-03 would result
    in two interval objects holding the daily working hours for the two days.
    """

    # Set start and end date-time
    from_date = from_date + ' 00:00:00.000'
    to_date = to_date + ' 23:59:59.999'

    # Calculate intervals
    intervals = b_date.get_intervals_for_epochs(
        b_date.timestamp_to_epoch(from_date),
        b_date.timestamp_to_epoch(to_date),
        'day'
    )

    # Transform to internal database format
    intervals = [
        {
            'range': (  # A date-time tuple from 00:00 of that day until 23:59
                b_date.dto_to_timestamp(interval[0], '%Y-%m-%dT%H:%M:%S'),
                b_date.dto_to_timestamp(interval[1], '%Y-%m-%dT%H:%M:%S')
            ),
            'w_hours': None  # A placeholder for the actual working hours
        }
        for interval in intervals
    ]
    return intervals


def load_database(_file):
    """Load file-based database, i.e., a JSON document.

    This file is used to store previously fetched API-results.
    """
    try:
        return load(open(_file))
    except Exception:
        return {}


def save_database(db, _file):
    """Save file-based database, i.e., a JSON document.

    This file is used to store previously fetched API-results.
    """
    dump(db, open(_file, 'w'), indent=4, sort_keys=True)


def get_db_key_for_interval(interval):
    """Calculate a database key for the given interval object."""
    return '>>'.join(interval['range'])


def initialize_api_client(api_client, api_credential_file):
    """API client initialization.api_client

    Initialize an API client with the given credential file.
    """

    return api_client(load(open(api_credential_file, 'r')))


def parse_cmd_line():
    """Command line parser and options."""

    prs = b_cmdprs.TemplateArgumentParser('Get average daily working hours')
    prs.add_file_in(arg='-o', help='Database file')
    prs.add_file_in(arg='-c', help='Credentials file')
    prs.add_option(arg='-f', help='From day (YYYY-MM-DD)')
    prs.add_option(arg='-t', help='To day (YYYY-MM-DD)')
    return prs.parse_args()
