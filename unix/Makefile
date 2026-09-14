# GNU make, GCC with C99 support, and the system X11 development libraries.
CC ?= gcc
PREFIX ?= /usr/local
DESTDIR ?=
CORE = ../PC110Atlas/Vendor/PC110Core
CPPFLAGS += -I$(CORE)/include
CFLAGS ?= -O2 -std=c99 -Wall -Wextra
X11_CFLAGS ?=
X11_LIBS ?= -lX11
LDLIBS = $(X11_LIBS) -lm

all: build/pc110-atlas-unix

build:
	mkdir -p build

build/pc110_core.o: $(CORE)/pc110_core.c $(CORE)/include/PC110Core/PC110Core.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

build/atlas_x11.o: atlas_x11.c pixel.h $(CORE)/include/PC110Core/PC110Core.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) $(X11_CFLAGS) -c $< -o $@

build/pc110-atlas-unix: build/atlas_x11.o build/pc110_core.o
	$(CC) $(CFLAGS) $(LDFLAGS) $^ $(LDLIBS) -o $@

build/test-portable: tests/test_portable.c pixel.h build/pc110_core.o
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $< build/pc110_core.o -lm -o $@

check: build/test-portable
	./build/test-portable

install: all
	mkdir -p "$(DESTDIR)$(PREFIX)/bin" "$(DESTDIR)$(PREFIX)/share/doc/pc110-atlas-unix"
	cp build/pc110-atlas-unix "$(DESTDIR)$(PREFIX)/bin/"
	cp README.md "$(DESTDIR)$(PREFIX)/share/doc/pc110-atlas-unix/"

clean:
	rm -f build/atlas_x11.o build/pc110_core.o build/pc110-atlas-unix build/test-portable

.PHONY: all check install clean
