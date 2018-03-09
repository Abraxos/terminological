# Terminological

Terminological is a python library for NCurses programming. It is partly inspired by [Termbox](https://github.com/nsf/termbox) because I really liked the simplicity and interface provided by it, but needed something available based on just the basic tools in the Python Standard Library as well as something capable of working with mouse-clicks.

## Installation & Setup

1) Clone the git repo

```
$ git clone git@github.com:Abraxos/terminological.git
```

2) Install terminological using pip

```
$ pip3 install ./terminological
```

Note that its probably best to either install it in a virtualenv (see Development section below) or with the `--user` parameter to only install it for the current user.

## Development and Testing

1) Clone the git repo

```
$ git clone git@github.com:Abraxos/terminological.git
```

2) Create the [virtualenv](https://virtualenv.pypa.io/en/stable/) (I recommend using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

```
$ mkvirtualenv --python=$(which python3) terminological-venv
(terminological-venv)$
```

3) Install the package, which also installs the pre-requisites

```
(terminological-venv)$ pip install -e ./terminological
```

Now you should be able to run the tests and go nuts from there:

**Run all tests**

```
(terminological-venv)$ pytest -s -vv terminological/tests/
```

**Run all tests with coverage**

```
(terminological-venv)$ pytest -s -vv --cov-report=html --cov=terminological terminological/tests/
```

**Run all the unit tests** _Right now all the tests are unit tests, but eventually there may be integration tests._

```
(terminological-venv)$ pytest -s -vv --cov-report html --cov=terminological terminological/tests/unit
```

## Examples
