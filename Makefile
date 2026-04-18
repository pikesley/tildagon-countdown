APP = $(shell basename $$(pwd))

all: format test clean

push: convert-conf
	python base_scripts/pusher.py

mkdir:
	-python -m mpremote mkdir apps/${APP}

connect:
	python -m mpremote

deploy: mkdir push connect

uninstall:
	python -m mpremote fs rm -r :/apps/${APP}

excludes:
	python base_scripts/excluder.py

convert-conf: fix-asset-path
	python base_scripts/conf_yaml_to_json.py

fix-asset-path:
	PYTHONPATH=. python templates/asset_path_fixer.py

test-release:
	bash base_scripts/build-release.sh deploy

simulate-release: clean-simulator
	bash base_scripts/build-release.sh simulate

release:
	python base_scripts/releaser.py

scrub-badge:
	-python -m mpremote fs rm -r apps/
	python -m mpremote mkdir :/apps

scrub-tags:
	bash base_scripts/scrub-tags.sh

simulate: clean-simulator convert-conf
	bash base_scripts/simulate.sh

clean-simulator:
	bash base_scripts/clean-simulator.sh

skellify:
	bash base_scripts/skellify.sh

format:
	ruff format
	ruff check --fix

test:
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .ruff_cache -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;

build:
	docker build \
		--build-arg APP=${APP} \
		--tag ${APP} .

run:
	docker run \
		--name ${APP} \
		--hostname ${APP} \
		--volume $(shell pwd):/opt/${APP} \
		--volume ${HOME}/.config:/root/.config \
		--interactive \
		--tty \
		--rm \
		${APP} \
		bash
