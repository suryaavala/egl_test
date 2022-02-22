.PHONY: check-all check-lint check-security check-types clean docker-entry-bash setup-dev install-git-hooks install-pipenv install-py-requirements install-py-dev-req install-py-dev-as-sys load-pipenv-shell setup-dev pytest test-coverage test-serving test-local test-local-docker train server-build serve server-logs server-stop-clean

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = linear_regressor
PYTHON_INTERPRETER = python3
HOST = "0.0.0.0"
PORT = 5000
#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Setup Local Dev environment
setup-dev: install-pipenv install-py-dev-req load-pipenv-shell install-git-hooks

## Install Git Hooks
install-git-hooks:
	pre-commit install

## loads a docker container at a bash entrypoint with current repo mounted
docker-entry-bash:
	docker build -t builder --file builder.Dockerfile .
	docker run -it --entrypoint bash --mount type=bind,source=$(CURDIR),target=/app builder:latest

## Install dev requirements as a virtual env (including actual package/runtime requirements)
install-py-dev-req:
	pipenv install --dev

## Install dev requirements at system level
install-py-dev-as-sys:
	pipenv install --dev --system

## Install Pipenv
install-pipenv:
	pip3 install pipenv==2022.1.8

## Load Pipenv shell
load-pipenv-shell:
	pipenv shell

## Install Python Prod Dependencies
install-py-requirements:
	pipenv install --system --deploy


## intall the package in root dir
install: clean
	python setup.py install

## Delete all compiled Python files, test files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -type f -name '*.egg' -exec rm -fr {} +
	find . -type d -name '*.egg-info' -exec rm -fr {} +

	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache

## Lint using flake8
check-lint:
	flake8 linear_regressor

## security check using bandit
check-security:
	bandit -l --recursive -x ./tests -r .

## type checks with mypy
check-types:
	mypy linear_regressor

## checks code for linting, security and type errors
check-all: check-lint check-types check-security

## unit tests code with pytest
pytest:
	pytest -vvv --capture=tee-sys --junitxml=pytest_report.xml

## check code coverage quickly with the default Python
test-coverage:
	coverage run -m pytest
	coverage report -m
	coverage html

## test serving by sending some sample requests
test-serving: server-stop-clean serve
	./scripts/test_local_server.sh "0.0.0.0" "$(PORT)"
	make server-stop-clean

## runs check-all, pytest, coverage, test-serving; use when testing locally
test-local: check-all pytest test-coverage test-serving

## runs check-all, pytest, coverage, test-serving; use when testing locally in a docker
test-local-docker:
	docker build -t builder --file builder.Dockerfile .
	-docker run -i \
		--mount type=bind,source=$(CURDIR),target=/app \
		--entrypoint make \
		builder:latest -- test-local

	make test-serving

## trains linear_regressor model
train:
	PYTHONPATH=. pipenv run python3 main.py train

## builds linear_regressor server image as linear_regressor_server:latest
server-build:
	docker build -t linear_regressor_server --file server.Dockerfile .

## builds and servers the linear_regressor in a docker container
serve: server-build
	docker run -i -p $(PORT):$(PORT) --env PORT=$(PORT) -d --name="linear_regressor" linear_regressor_server:latest

## follow linear_regressor server logs (if running)
server-logs:
	docker logs -f linear_regressor

## stop and remove running/dangling linear_regressor servers
server-stop-clean:
	docker stop linear_regressor || true
	docker rm linear_regressor || true


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
