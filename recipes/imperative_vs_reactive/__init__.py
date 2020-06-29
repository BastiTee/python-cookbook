"""Imperative versus Reactive.

This gist contains an _imperative_ and a _reactive_ Python module fetching
data from the Toggl API
https://github.com/toggl/toggl_api_docs/blob/master/toggl_api.md)
to obtain the average daily working hours. All code snippets are
documented and should be self explanatory.

The reactive implementation uses the RxPy (https://github.com/ReactiveX/RxPY),
a Python-implementation of the ReactiveX API (http://reactivex.io/).

Best start with the [imperative version](#file-get_daily_average_imp-py) to see how the naive loop-based implementation behaves and follow up with the [reactive version](#file-get_daily_average_rx-py). Both implementations share [common functionality](#file-toggl_api_commons-py). The contained database "layer" was only introduced for sake of having a little more complexity. A corresponding [test-suite](#file-test_get_daily_average-py) compares both versions. For better readability the imperative version does not utilize parallel processing.

**Install**

    python3 -m pip install -r requirements.txt

**Run imperative vs. reactive benchmark**:

    python3 test_get_daily_average.py

**Fetch real data**:

Before accessing the Toggl API, you need to setup an API key and prepare a credential-file. See the [default-file](#file-credentials-json-default) for further reference.

    cp credentials.json.default credentials.json
    vi credentials.json  # add your actual credentials
    python3 get_daily_average_rx \
        -o db.json \
        -c credentials.json \
        -f 2018-04-01 \
        -t 2018-05-01 \

with

    usage: Get average daily working hours [-h] [-o INPUT] [-c INPUT] [-f VALUE] [-t VALUE]

    optional arguments:
      -h, --help  show this help message and exit
      -o INPUT    Database file
      -c INPUT    Credentials file
      -f VALUE    From day (YYYY-MM-DD)
      -t VALUE    To day (YYYY-MM-DD)
"""
