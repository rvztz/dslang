export PYTHONPATH:=${PYTHONPATH}:/dslang/

clean:
	find . -type d -name __pycache__ -exec rm -r {} \+
	echo ${dlang}

install:
	python -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

test_parser:
	python test_parser.py

test_lexer:
	python test_lexer.py
