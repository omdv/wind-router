# Project settings
PROJECT := WindRouter
PACKAGE := windrouter
REPOSITORY := omdv/wind-router

# Project paths
# PACKAGES := $(PACKAGE) tests
# CONFIG := $(wildcard *.py)
# MODULES := $(wildcard $(PACKAGE)/*.py)

.PHONY: install
install:
	conda env create --file conda.yml

.PHONE: test
test:
	python -m unittest discover -v

.PHONE: commit
commit:
	conda update -y --all
	conda env export --no-builds > conda.yml