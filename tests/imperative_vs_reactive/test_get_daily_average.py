#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test suite for the daily average Toggl API process."""

from random import random
from tempfile import NamedTemporaryFile
from time import sleep, time
from unittest import TestCase

from get_daily_average_imp import get_avg_daily_working_hours as imp
from get_daily_average_rx import get_avg_daily_working_hours as rx


class TestSuite(TestCase):

    def test_integration(self):

        # Between 23th of April and 4th of May we spend an average
        # of 3.981 simulated hours at work for the given 4-hour contract.
        from_day = '2018-04-23'
        to_day = '2018-05-04'
        expected_worktime_average = 3.98056125
        expected_workdays = 10

        # Run test for imperative implementation using a mocked client
        now = time()
        tmp_file_imp = NamedTemporaryFile()
        result_imp = imp(from_day, to_day, tmp_file_imp.name,
                         MockedTogglApiClient)
        time_imp = time() - now
        print('----')

        # Run test for reactive implementation using a mocked client
        now = time()
        tmp_file_rx = NamedTemporaryFile()
        result_rx = rx(from_day, to_day, tmp_file_rx.name,
                       MockedTogglApiClient)
        time_rx = time() - now
        print('----')

        # Check results
        self.assertEquals(result_imp,
                          (expected_worktime_average, expected_workdays))
        self.assertEquals(result_rx,
                          (expected_worktime_average, expected_workdays))

        # Print results
        print('imp-result = {} h @{} days (took: {} sec)'.format(
            round(result_imp[0], 2), result_rx[1], round(time_imp, 4)))
        print('rx-result = {} h @{} days (took: {} sec)'.format(
            round(result_rx[0], 2), result_rx[1], round(time_rx, 4)))
        print('rx speed-up = {}'.format(time_imp / time_rx))


class MockedTogglApiClient():
    """A mocked Toggl API client.

    Assuming that we have a 4-hour work contract, the Toggl API might
    return values between 3.8 and 4.2 hours of total working hours per day.
    Toggl API responses take between 0.0 and 0.5 seconds in our mocked version.
    """

    def __init__(self, credentials=None):
        self.fake_values = {
            '2018-04-23T00:00:00>>2018-04-23T23:59:59': 14853641,  # 4.1260 h
            '2018-04-24T00:00:00>>2018-04-24T23:59:59': 13725371,
            '2018-04-25T00:00:00>>2018-04-25T23:59:59': 14209405,
            '2018-04-26T00:00:00>>2018-04-26T23:59:59': 13969792,
            '2018-04-27T00:00:00>>2018-04-27T23:59:59': 14591221,
            '2018-04-28T00:00:00>>2018-04-28T23:59:59': 0,
            '2018-04-29T00:00:00>>2018-04-29T23:59:59': 0,
            '2018-04-30T00:00:00>>2018-04-30T23:59:59': 14012216,
            '2018-05-01T00:00:00>>2018-05-01T23:59:59': 14802751,
            '2018-05-02T00:00:00>>2018-05-02T23:59:59': 14752767,
            '2018-05-03T00:00:00>>2018-05-03T23:59:59': 14601954,
            '2018-05-04T00:00:00>>2018-05-04T23:59:59': 13781087
        }

    def get_working_hours_for_range(self, range_from, range_to):
        #  A simulated API request takes between 0.0 and 0.5 seconds ...
        sleep(random() / 2)
        #  ... and returns a fake value.
        return self.fake_values.get('>>'.join([range_from, range_to]), 0)


if __name__ == '__main__':
    TestSuite().test_integration()
