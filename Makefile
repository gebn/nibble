clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf nibble.egg-info
	rm -rf dist
	rm -rf build
	rm -rf .eggs
	rm -f .coverage
	rm -f nibble/expression/{parser.out,parsetab.py,parsetab.pyc}
