#!/bin/sh
set -e  # Always exit on non-zero return codes
cd "$( cd "$( dirname "$0" )"; pwd )"

# Check python and pipenv installation
[ -z "$( command -v python3 )" ] && { echo "python3 not available."; exit 1; }
[ -z "$( command -v pipenv )" ] && { echo "pipenv not available."; exit 1; }

export PIPENV_VERBOSITY=${PIPENV_VERBOSITY:--1}
export PIPENV_VENV_IN_PROJECT=${PIPENV_VENV_IN_PROJECT:-1}
export PIPENV_IGNORE_VIRTUALENVS=${PIPENV_IGNORE_VIRTUALENVS:-1}
export PYTHONPATH=${PYTHONPATH:-.}
export LC_ALL=${PYPE_ENCODING:-${LC_ALL}}
export LANG=${PYPE_ENCODING:--${LANG}}

rm -rf .venv
pipenv install --dev --skip-lock
