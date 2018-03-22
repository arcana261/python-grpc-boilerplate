.PHONY: python pipenv check install clean generate test coverage build

include common.in

EXEC := $(if $(filter-out 0,$(USE_SYSTEM_PYTHON)),/bin/sh -c,./build/python/bin/exec)
EXEC_FIRST := $(firstword $(EXEC))
PROTOS := $(wildcard src/**/*.proto)
PB2S := $(addsuffix _pb2.py,$(basename $(PROTOS)))
PB2_GRPCS := $(addsuffix _pb2_grpc.py,$(basename $(PROTOS)))

build: generate

python:
ifeq ($(USE_SYSTEM_PYTHON),0)
	cd build/python && PROJECT_NAME=$(PROJECT_NAME) make install
endif
	/bin/sh -c 'export INSTALLED=0; if [ -f $(EXEC_FIRST) ]; then export INSTALLED="`$(EXEC) "which python"`"; fi; if [ "$$INSTALLED" = "" ]; then echo "python not found"; exit 1; fi'

pipenv: python
	/bin/sh -c 'export INSTALLED=0; if [ -f $(EXEC_FIRST) ]; then export INSTALLED="`$(EXEC) "which pip"`"; fi; if [ "$$INSTALLED" = "" ]; then echo "pip not found"; exit 1; fi'
	/bin/sh -c 'export INSTALLED=0; if [ -f $(EXEC_FIRST) ]; then export INSTALLED="`$(EXEC) "pip show pipenv 2> /dev/null"`"; fi; if [ "$$INSTALLED" = "" ]; then $(EXEC) "pip install --user pipenv"; fi'

check: pipenv
	$(EXEC) "pipenv check"

install: Pipfile.lock

Pipfile.lock: Pipfile | pipenv
ifeq ($(RELEASE_BUILD),0)
	$(EXEC) "pipenv install --dev"
else
	$(EXEC) "pipenv install"
endif

clean:
	-./build/python/bin/exec "pipenv --rm"
	-pipenv --rm
	-rm -fv Pipfile.lock
	-rm -fv $(PB2S) $(PB2_GRPCS)
	-cd build/python && PROJECT_NAME=$(PROJECT_NAME) make clean

generate: $(PB2S) $(PB2_GRPCS)

.SECONDEXPANSION:
$(PB2S) $(PB2_GRPCS): $$(patsubst %_pb2_grpc.py,%.proto,$$(patsubst %_pb2.py,%.proto,$$(firstword $$@))) Pipfile.lock | install
	$(EXEC) "pipenv run python -m grpc_tools.protoc -Isrc --python_out=src --grpc_python_out=src $<"

test: build
	$(EXEC) "cd src && pipenv run python -m unittest"

coverage: build
	$(EXEC) "cd src && pipenv run py.test --cov=."

lint: build
	$(EXEC) "pipenv run pycodestyle --show-source --show-pep8 --config=.pycodestyle src"
