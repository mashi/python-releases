[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![github-actions](https://github.com/mashi/python-releases/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/mashi/python-releases/actions)


# Description
This repository implements a web scraper and data visualization.

The interactive plot is uploaded to the Heroku platform ([link](https://python-releases.herokuapp.com/)).

![visualization](img/visualization.png)


## Softaware and Tools
The development uses:
1. Version control with git to track changes.

1. A pre-commit to maintain the quality of the code. It helps identify issues, for example, code formatting, *before* files are added to the version control. Check the `.pre-commit-config.yaml` for the complete list of verifications.

1. Here, CI/CD tools are implemented using GitHub actions. The CI process is triggered by code changes and
executes the unittests defined in the test folder.

1. The CD process is triggered when new code is added to the main branch and new releases are automatically uploaded to Heroku using the [github integration](https://devcenter.heroku.com/articles/github-integration) option enabled.

1. For maintenance:
    1. the renovatebot is configured to keep packages up to date.
    1. Scheduled tests are configured to identify issues and external changes in this repository code (for example, changes on the source site).


## Instructions (Development)
Create a virtual environment and install the required packages with
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install wheel
pip install -r requirements-dev.txt
pre-commit install
```


### Tests
To execute tests, type
```
python -m unittest discover
```
