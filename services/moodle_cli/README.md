# Moodle CLI

This is a simple CLI implented as a Python package to automate tasks on Moodle instances. The CLI can be installed and invoked to display help with available commands as follows:

```bash
$ pip install .
$ moodle-cli
```

When developing, you may want to install the project in editable mode:

```bash
$ pip install -e .
```

The code can be linted and tested as well:

```bash
$ pip install .[test]
$ flake8
$ pytest
```

Code coverage reports can also be generated when running tests:

```bash
$ pytest --cov=moodlecli --cov-report=term --cov-report=html
```
