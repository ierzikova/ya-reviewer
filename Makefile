VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test: install
	pytest

coverage: install
	coverage run -m pytest
	coverage report -m

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf $(VENV)
	rm -f .coverage
