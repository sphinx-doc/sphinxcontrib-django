# Contributing

Pull requests are always welcome!

## Development setup

Install all requirements of the development setup with the extras `dev`,
`test`, `doc` and `optional`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev,test,doc,optional]
pre-commit install
```

## Tests

Run the tests and generate the coverage report with:

```bash
coverage run
coverage html
```

## Code style

Formatting and linting are enforced by [black](https://github.com/psf/black)
and [ruff](https://github.com/astral-sh/ruff) via pre-commit hooks, which run
automatically on every commit after `pre-commit install`.

## Documentation

Build the documentation with:

```bash
cd docs
make html
```

The documentation is automatically deployed to
[Read the Docs](https://sphinxcontrib-django.readthedocs.io/).

## Pull requests

- Base your work on the `main` branch.
- Add an entry to the `Unreleased` section of `CHANGES.rst` for user-facing
  changes.
- Reference related issues in the pull request description.
