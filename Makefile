DOCKER_NAME=scp_graphql
VERSION=$(shell cat VERSION)
DOCKER_IMAGE=${DOCKER_NAME}:${VERSION}
DOCKER_REPO=826410511458.dkr.ecr.eu-west-1.amazonaws.com

install:
	pipenv install

run:
	cd scp && python server.py

docker_build:
	docker build \
		-t ${DOCKER_IMAGE} .
