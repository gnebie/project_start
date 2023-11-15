

sphinx-start:
	sphinx-quickstart docs

sphinx-build:
	(cd docs; make html)

init:
    pip install -r requirements.txt

test:
    py.test tests

create-executable:
	echo "see pyinstaller doc : pyinstaller --onefile cli.py"
	echo "https://realpython.com/pyinstaller-python/"


.PHONY: init test
