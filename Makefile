VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install:
    $(PYTHON) -m venv $(VENV)
    $(PIP) install -r requirements.txt

test:
    source $(VENV)/bin/activate
    pytest

coverage:
    coverage run -m pytest
    coverage report -m

clean:
    rm -rf __pycache__
    rm -rf $(VENV)