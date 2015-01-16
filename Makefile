SHELL=/bin/bash

all:
	@./make build

install:
	@./make install

uninstall:
	@./make remove

clean:
	@./make clean

distclean:
	@./make clean

help:
	@./make help

pot:
	@./make pot

po:
	@./make po
