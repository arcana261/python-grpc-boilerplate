.PHONY: .requisite-check prepare build install clean help

ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VERSION := $(shell cat snap.in/snapcraft.yaml | grep "\s*version:" | sed "s|\s*version:\s*||g" | sed "s|'||g" | sed "s|\s||g")
PROJECT_NAME ?= NONE
BIN_IN := $(wildcard bin.in/*)
BIN_OUT := $(addprefix bin/,$(notdir $(BIN_IN)))
SNAP_NAME := $(subst $${PROJECT_NAME},$(PROJECT_NAME),$(shell cat snap.in/snapcraft.yaml | grep "\s*name:" | sed "s|\s*name:\s*||g" | sed "s|'||g" | sed "s|\s||g"))
SNAP_PACKAGE := $(SNAP_NAME)_$(VERSION)_amd64.snap

build: .requisite-check $(SNAP_PACKAGE)

prepare: .requisite-check snap/snapcraft.yaml

install: .requisite-check .INSTALL $(BIN_OUT)

clean: .requisite-check
	-sudo rm -rfv snap
	-rm -rfv bin
	-sudo rm -rfv parts
	-sudo rm -rfv prime
	-sudo rm -rfv stage
	-rm -rfv .INSTALL
	-sudo snap remove $(SNAP_NAME)
	-sudo rm -rfv $(SNAP_PACKAGE)

help:
	@echo "build and install python environment tailored for specific project"
	@echo "usage:"
	@echo "    PROJECT_NAME=my-project make"
	@echo "    PROJECT_NAME=my-project make install"
	@echo "requires:"
	@echo "    docker"
	@echo "    snapd"
	@echo "    amd64 architecture"
	@echo "    user should be in sudoers and docker group"
	@echo "commands:"
	@echo "    prepare: prepare snap/snapcraft.yaml"
	@echo "    build:   default target, compile python from source and build snap package"
	@echo "    install: install python snap package"
	@echo "    clean:   clean all built files and remove snap package from system"
	@echo "    help:    show this help message"

snap/snapcraft.yaml: snap.in/snapcraft.yaml | snap
	cat $< | sed -e "s|\$${PROJECT_NAME}|$(PROJECT_NAME)|g" > $@

snap:
	mkdir -p snap

$(SNAP_PACKAGE): snap/snapcraft.yaml
	docker run --rm -v $(ROOT_DIR):$(ROOT_DIR) -w $(ROOT_DIR) snapcore/snapcraft snapcraft

.INSTALL: $(SNAP_PACKAGE)
	sudo snap install $< --dangerous --classic
	touch .INSTALL

.SECONDEXPANSION:
$(BIN_OUT): $(addprefix bin.in/,$$(notdir $$@)) | bin
	cat $< | sed -e "s|\$${SNAP_NAME}|$(SNAP_NAME)|g" > $@
	chmod +x $@

bin:
	mkdir -p bin

.requisite-check:
ifeq ($(shell which docker),)
	$(error docker not found, please install docker)
endif
ifeq ($(shell which snap),)
	$(error snapd not found, please install snapd)
endif
ifeq ($(shell which sudo),)
	$(error sudo command not found, please ensure sudo is installed)
endif
ifeq ($(shell which uname),)
	$(error uname command not found, please ensure availability of uname command)
endif
ifeq ($(shell which cat),)
	$(error cat command not found, please ensure availability of cat command)
endif
ifeq ($(shell which grep),)
	$(error grep command not found, please ensure availability of grep command)
endif
ifeq ($(shell which sed),)
	$(error sed command not found, please ensure availability of sed command)
endif
ifeq ($(shell which mkdir),)
	$(error mkdir command not found, please ensure availability of mkdir command)
endif
ifeq ($(shell which groups),)
	$(error groups command not found, please ensure availability of groups command)
endif
ifeq ($(shell which chmod),)
	$(error chmod command not found, please ensure availability of chmod command)
endif
ifeq ($(shell which sh),)
	$(error sh not found, please ensure availability of sh command)
endif
ifeq ($(shell which bash),)
	$(error bash not found, please ensure availability of bash command)
endif
ifeq ($(shell which touch),)
	$(error touch not found, please ensure availability of touch command)
endif
ifeq ($(shell which rm),)
	$(error rm not found, please ensure availability of rm command)
endif
ifeq ($(PROJECT_NAME),NONE)
	$(error provide PROJECT_NAME environment correctly, like PROJECT_NAME=foo make)
endif
ifeq ($(shell groups | grep "docker"),)
	$(error user should be in docker group to proceed)
endif
ifneq ($(shell uname -i),x86_64)
	$(error this build is only supported for x86_64 systems)
endif
ifeq ($(shell snap list | grep "^$(SNAP_NAME)\s"),)
	-rm -fv .INSTALL
endif
