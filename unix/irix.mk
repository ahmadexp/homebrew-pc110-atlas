# Run with SGUG GCC and GNU make from the unix directory.
CC = /usr/sgug/bin/gcc
PREFIX = /usr/sgug
CFLAGS = -O2 -std=c99 -mabi=n32 -mips3 -Wall -Wextra
X11_CFLAGS = -I/usr/include
X11_LIBS = -L/usr/lib32 -lX11
include Makefile
