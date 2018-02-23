.PHONY: dev_generate dev_install dev

NAME=proto
PROTO_DIR=proto

DOCKER=docker
TOUCH=touch
MKDIR=mkdir
RM=rm
DEST_DIR=/opt/project

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DOCKER_RUN=$(DOCKER) run -it --rm -e "uid=`id -u`" -v $(ROOT_DIR):$(DEST_DIR) -v $(ROOT_DIR)/.venv:/root/.local/share/virtualenvs $(NAME)_dev
PROTOC=pipenv run python -m grpc_tools.protoc
PROTOS=$(wildcard $(PROTO_DIR)/*.proto)
PB2S=$(patsubst %.proto,%_pb2.py,$(PROTOS))
GRPC_PB2S=$(patsubst %.proto,%_pb2_grpc.py,$(PROTOS))
HAS_DOCKER_IMAGE=$(shell docker images | grep -c proto_dev)

dev: dev_generate
dev_generate: .pre-check $(PB2S) $(GRPC_PB2S)
dev_install: .pre-check .touch/.dev_docker Pipfile
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv install --dev && chown -R $$uid:$$uid /root/.local/share/virtualenvs && chown $$uid:$$uid $(DEST_DIR)/Pipfile.lock'

.pre-check: .venv
ifeq ($(HAS_DOCKER_IMAGE), 0)
	rm -rfv .touch 2>/dev/null; true
endif

$(PROTO_DIR)/%_pb2.py $(PROTO_DIR)/%_pb2_grpc.py: $(PROTO_DIR)/%.proto .touch/.dev_dep
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && $(PROTOC) -Iproto/ --python_out=proto/ --grpc_python_out=proto/ $< && chown $$uid:$$uid $(patsubst %.proto,%_pb2.py,$<) && chown $$uid:$$uid $(patsubst %.proto,%_pb2_grpc.py,$<)'

.touch/.dev_dep: .touch/.dev_docker Pipfile
	$(DOCKER_RUN) bash -c 'cd $(DEST_DIR) && pipenv install --dev && chown -R $$uid:$$uid /root/.local/share/virtualenvs && chown $$uid:$$uid $(DEST_DIR)/Pipfile.lock'
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_dep

.touch/.dev_docker: .venv .touch/.dev_build
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_docker

.venv:
	$(MKDIR) -p .venv
	$(RM) .touch/.dev_dep 2>/dev/null; true

.touch/.dev_build: dev/Dockerfile
	$(DOCKER) build -t $(NAME)_dev dev/
	$(MKDIR) -p .touch
	$(TOUCH) .touch/.dev_build


