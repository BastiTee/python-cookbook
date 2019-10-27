#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ReactiveX-style Toggl API requests to obtain avg daily working hours."""

import toggl_api_commons as com
from rx import Observable, Observer, config
from rx.concurrency import ThreadPoolScheduler


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

    # Setup a lock that we will use later to wait for the whole observerable
    # chain to be finished. As of v1.5.8 a built-in blocking subscribe
    # method was not available yet.
    # See https://github.com/ReactiveX/RxPY/issues/203 and
    # https://github.com/ReactiveX/RxPY/pull/232
    # Without this mechanism the method would return (and the program exit)
    # before the process chain is completed.
    done_lock = config['concurrency'].Event()

    # Convert given time span to daily intervals
    intervals = com.create_input_ranges(from_day, to_day)

    # Create an Observable operator that will transform our input
    # on each processing step troughout the Observable chain.
    operator = ObservableOperator(intervals)
    # Create a statistics observer that will pick up the API results
    # and generate our final result value.
    observer = StatisticsObserver(done_lock)

    db = com.load_database(result_file)

    (
        # Create an observable that creates a tick every 50 ms.
        # We use this to avoid the API limit of Toggl.
        # https://ninmesara.github.io/RxPY/api/operators/interval.html
        Observable.interval(75)
        # Continue to evaluate the ticks until (i)nterval index reached the
        # end of the input interval list.
        .take_while(lambda i: i < operator.get_interval_count())
        # Flat map (i)nterval index to the actual interval from the input list.
        # Hint: Order using flat_map without concurrecy is not kept by design.
        # See: https://bit.ly/2shQ5L4
        .flat_map(lambda i: operator.pick_input_range(i))
        # Map interval to database value that might or might not exist yet.
        .flat_map(lambda interval: operator.read_from_database(db, interval))
        # Map interval to API request.
        .flat_map(lambda interval: operator.request_api_if_required(
            interval, api_access))
        # Map interval holding the result of the API request to database
        .flat_map(lambda interval: operator.write_to_database(db, interval))
        # Subscribe with an observer to the observable chain.
        .subscribe(observer)
    )

    # Instead of actively waiting here, we wait for a signal on the done_lock.
    # This is signalled by the StatisticsObserver when all intervals are
    # processed or an error occured.
    done_lock.wait()

    # Save and return...
    com.save_database(db, result_file)
    return observer.get_result()


class StatisticsObserver(Observer):
    """An observer collecting working hour statistics."""

    def __init__(self, done_lock=None):
        self.whours = []  # Holds all observed working hours not equal to zero
        self.avg_whours = 0  # Average working hours
        self.done_lock = done_lock  # Done lock to signal process completion

    def on_next(self, interval):
        # Emitted by the last observable in the main process chain
        if interval['w_hours'] > 0:
            self.whours.append(interval['w_hours'])

    def on_completed(self):
        # Handle emitted completion signal from observable chain
        # Here: Calculate average working hours and free process lock
        self.avg_whours = sum(self.whours) / len(self.whours) / 1000 / 60 / 60
        self.done_lock.set()

    def on_error(self, error):
        # Free process lock on errors
        print(error)
        self.done_lock.set()

    def get_result(self):
        return self.avg_whours, len(self.whours)


class ObservableOperator():
    """Main observable chain operator.

    This operator takes objects from a previous mapping step,
    manipulates the data and emits new Observables.
    """

    def __init__(self, intervals):
        self.intervals = intervals
        # A thread-pool for concurrent processing
        self.scheduler = ThreadPoolScheduler(10)

    def _to_observable(self, object):
        """Factory method to consistently create new Observables."""
        return Observable.just(object).observe_on(self.scheduler)

    def pick_input_range(self, index):
        """Take a list index and emit the input interval for it."""
        interval = self.intervals[index]
        print('[INIT] Selected interval:', interval)
        return self._to_observable(interval)

    def read_from_database(self, db, interval):
        """Take an interval and emit the database entry for it or None."""
        db_interval = db.get(com.get_db_key_for_interval(interval), None)
        return self._to_observable(
            db_interval if db_interval is not None else interval)

    def write_to_database(self, db, interval):
        """Take an interval object, store and then re-emit it."""
        db[com.get_db_key_for_interval(interval)] = interval
        return self._to_observable(interval)

    def request_api_if_required(self, interval, api_client):
        """Take an interval and, if necessary, call API and emit result."""
        # Skip interval if we have fetched the working hours before
        if interval is not None and interval['w_hours'] is not None:
            print('[API-REQ] {}'.format('Skipped.'))
            return self._to_observable(interval)
        # Invoke API request
        try:
            interval['w_hours'] = api_client.get_working_hours_for_range(
                interval['range'][0], interval['range'][1])
        except Exception as e:
            return Observable.throw(e)
        print('[API-REQ] Received data: {} > {} = {}'.format(
            interval['range'][0], interval['range'][1], interval['w_hours']))
        return self._to_observable(interval)

    def get_interval_count(self):
        return len(self.intervals)


if __name__ == '__main__':
    # If run directly, parse the command line and invoke the core
    # function that returns the average daily working hours for the given
    # time span.
    args = com.parse_cmd_line()
    whours, days = get_avg_daily_working_hours(
        args.f, args.t, result_file=args.o, api_credential_file=args.c)
    print('daily-workinghours-average = {} h ({} days)'.format(
        round(whours, 2), days))
