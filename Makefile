export PYTHONPATH:=${PYTHONPATH}:/dslang/ 

clean:
	find . -type d -name __pycache__ -exec rm -r {} \+

install:
	python -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

test_parser:
	python tests/test_parser.py

test_lexer:
	python tests/test_lexer.py
