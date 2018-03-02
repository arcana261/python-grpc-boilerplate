.PHONY: dev dev-generate dev-install dev-up dev-down clean

PROTO_DIR?=proto

DOCKER=docker
TOUCH=touch
MKDIR=mkdir
RM=rm
DEST_DIR=/opt/project

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
NAME:=$(notdir $(ROOT_DIR))
DOCKER_RUN=$(DOCKER) run -it --rm -e "uid=`id -u`" -e "ROOT=$(ROOT_DIR)" -e "NAME=$(NAME)" -v $(ROOT_DIR):$(DEST_DIR) -v $(ROOT_DIR)/.venv:/root/.local/share/virtualenvs -v /var/run/docker.sock:/var/run/docker.sock $(NAME)_dev
PROTOC=pipenv run python -m grpc_tools.protoc
PROTOS=$(wildcard $(PROTO_DIR)/*.proto)
PB2S=$(patsubst %.proto,%_pb2.py,$(PROTOS))
GRPC_PB2S=$(patsubst %.proto,%_pb2_grpc.py,$(PROTOS))
HAS_DOCKER_IMAGE:=$(shell docker images | grep -c $(NAME)_dev)
HAS_DOCKER_GRPCC_IMAGE:=$(shell docker images | grep -c $(NAME)_grpcc_dev)

dev: .pre-check dev-generate dev-install
dev-generate: .pre-check $(PB2S) $(GRPC_PB2S)
dev-install: .pre-check .touch/.dev_dep
dev-up: .pre-check dev .touch/.dev_docker_compose
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv run docker-compose -f dev/docker-compose.yml up'
dev-down: .pre-check dev .touch/.dev_docker_compose
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv run docker-compose -f dev/docker-compose.yml down'

.pre-check: .venv
ifeq ($(HAS_DOCKER_IMAGE), 0)
	rm -rfv .touch 2>/dev/null; true
endif
ifeq ($(HAS_DOCKER_GRPCC_IMAGE),0)
	rm -rfv .touch 2>/dev/null; true
endif

clean:
ifneq ($(HAS_DOCKER_IMAGE), 0)
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv run docker-compose -f dev/docker-compose.yml down'
endif
	$(DOCKER) rmi $(NAME)_dev 2>/dev/null; true
	$(DOCKER) rmi $(NAME)_grpcc_dev 2>/dev/null; true
	$(RM) -fv $(PB2S) $(GRPC_PB2S) 2>/dev/null; true
	$(RM) -rfv .venv 2>/dev/null; true
	$(RM) -rfv .touch 2>/dev/null; true

.touch/.dev_docker_compose: .touch/.dev_docker dev/docker-compose.yml
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv run docker-compose -f dev/docker-compose.yml down'
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv run docker-compose -f dev/docker-compose.yml up --no-start'
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_docker_compose

$(PROTO_DIR)/%_pb2.py $(PROTO_DIR)/%_pb2_grpc.py: $(PROTO_DIR)/%.proto .touch/.dev_dep
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && $(PROTOC) -I. --python_out=. --grpc_python_out=. $< && chown $$uid:$$uid $(patsubst %.proto,%_pb2.py,$<) && chown $$uid:$$uid $(patsubst %.proto,%_pb2_grpc.py,$<)'

.touch/.dev_dep: .touch/.dev_docker Pipfile
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv install --dev && chown -R $$uid:$$uid /root/.local/share/virtualenvs && chown $$uid:$$uid $(DEST_DIR)/Pipfile.lock'
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_dep

.touch/.dev_docker: .venv .touch/.dev_build .touch/.dev_grpcc_build
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_docker

.venv:
	$(MKDIR) -p .venv
	$(RM) .touch/.dev_dep 2>/dev/null; true

.touch/.dev_build: dev/Dockerfile
	$(DOCKER) build -t $(NAME)_dev dev/
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_build

.touch/.dev_grpcc_build: dev/Dockerfile-grpcc
	$(DOCKER) build -t $(NAME)_grpcc_dev -f dev/Dockerfile-grpcc dev/
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_grpcc_build

