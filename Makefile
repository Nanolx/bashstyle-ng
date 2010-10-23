SHELL=/bin/bash

all:
	@./make build

install:
	@./make install

uninstall:
	@./make uninstall

clean:
	@./make clean

distclean:
	@./make distclean

help:
	@./make help

pot:
	@./make pot

po:
	@./make po
