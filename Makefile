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
	conda env create --file environment.yml

.PHONE: test
test:
	coverage run -m unittest discover
	coverage report -m