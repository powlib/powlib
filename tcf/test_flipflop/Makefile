# Default to verilog
TOPLEVEL_LANG ?= verilog

WPWD=$(shell sh -c 'pwd -W')
PWD=$(shell pwd)
POWLIB=$(PWD)/../..
COCOTB=$(POWLIB)/cocotb

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(POWLIB)/sim;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(POWLIB)/sim;$(PYTHONPATH)
endif

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(POWLIB)/hdl/*.v
    COMPILE_ARGS = -g 2001 -I $(POWLIB)/hdl/
    TOPLEVEL = powlib_std
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

MODULE=powlib_flipflop

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

