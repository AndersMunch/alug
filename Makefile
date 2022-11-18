.SUFFIXES:
.PHONY: test release

test:
	pytest

release:
	python setup.py bdist_wheel
