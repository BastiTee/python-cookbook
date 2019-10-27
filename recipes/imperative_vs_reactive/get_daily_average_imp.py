#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Imperative-style Toggl API requests to obtain avg daily working hours."""

import toggl_api_commons as com
from time import sleep


def get_avg_daily_working_hours(
    from_day,  # Beginning of observed time span
    to_day,  # End of observed time span
    result_file='toggl-api-results.json',  # Database file
    api_client=com.TogglApiClientDefault,  # API client implementation
    api_credential_file='credentials.json'  # API credential file
):
    """Core process workflow."""

    # Create an API accessor
    api_access = com.initialize_api_client(api_client, api_credential_file)
    # Convert given time span to daily intervals
    intervals = com.create_input_ranges(from_day, to_day)

    db = com.load_database(result_file)

    for interval in intervals:
        db_key = com.get_db_key_for_interval(interval)
        # Check if we have a database entry for that interval
        db_interval = db.get(db_key, None)
        db_interval = interval if db_interval is None else db_interval
        # Skip interval if we have fetched the working hours before
        if db_interval is not None and db_interval['w_hours'] is not None:
            print('[API-REQ] {}'.format('Skipped.'))
            continue
        # Invoke API request
        try:
            db_interval['w_hours'] = api_access.get_working_hours_for_range(
                interval['range'][0], interval['range'][1])
        except Exception as e:
            raise(e)
        print('[API-REQ] Received data: {} > {} = {}'.format(
            interval['range'][0], interval['range'][1], interval['w_hours']))
        sleep(0.2)  # Delay so we don't run into Toggl API limitations
        db[db_key] = db_interval  # Overwrite old value

    com.save_database(db, result_file)

    # Calculate average working hours using stored values
    total_workdays = 0
    total_workinghours = 0
    for interval in intervals:
        db_key = com.get_db_key_for_interval(interval)
        if not db[db_key]['w_hours'] or db[db_key]['w_hours'] == 0:
            continue  # Don't count zero-time days!
        total_workdays += 1
        total_workinghours += db[db_key]['w_hours']
    return (
        total_workinghours / total_workdays / 1000 / 60 / 60,
        total_workdays)


if __name__ == '__main__':
    # If run directly, parse the command line and invoke the core
    # function that returns the average daily working hours for the given
    # time span.
    args = com.parse_cmd_line()
    whours, days = get_avg_daily_working_hours(
        args.f, args.t, result_file=args.o, api_credential_file=args.c)
    print('daily-workinghours-average = {} h ({} days)'.format(
        round(whours, 2), days))
