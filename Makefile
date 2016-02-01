
ROOT = $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: all test integ run check install

all: run
run:
	cd $(ROOT); python main.py


test:
	cd $(ROOT); python -m unittest discover -s $(ROOT)/tests


integ:
	cd $(ROOT); python -m unittest discover -s $(ROOT)/integ


check:
	pep8 --show-source --show-pep8 "$(ROOT)/main.py" "$(ROOT)/emoji" "$(ROOT)/tests" "$(ROOT)/integ"


install:
	pip install -r requirements.txt
