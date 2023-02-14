VENV_PATH = /venv/bin/activate
ENVIRONMENT_VARIABLE_FILE = .env

init:
	pip3 install -r requirements.txt
env:
	python3 -m venv env
	source $(VENV_PATH)
	source $(ENVIRONMENT_VARIABLE_FILE)
install:
	python3 -m pip install --upgrade pip
setup:
	python3 main.py
