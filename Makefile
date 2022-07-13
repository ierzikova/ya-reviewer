VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test:
	pytest

coverage:
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report -m

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf $(VENV)
	rm -f .coverage
