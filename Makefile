ORG=konradmalik
VENV_NAME?=venv
MODULE=hlcpy
PYTHON=${VENV_NAME}/bin/python3

.PHONY: dist

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements-test.txt requirements.txt setup.py
	python3 -m virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements-test.txt -r requirements.txt
	touch $(VENV_NAME)/bin/activate

clean:
	rm -rf ./$(VENV_NAME)
	find . -type f -name "*.pyc" -delete

lint: venv
	${PYTHON} -m autopep8 --in-place -a -a -r tests ${MODULE}
	${PYTHON} -m autoflake --in-place --recursive --remove-all-unused-imports tests ${MODULE}
	${PYTHON} -m pylint --exit-zero tests ${MODULE}
	${PYTHON} -m mypy --ignore-missing-imports tests ${MODULE}

test: venv
	${PYTHON} -m pytest tests -sv

dist:
	rm -rf *.egg-info
	${PYTHON} setup.py sdist bdist_wheel
