# Default to verilog
TOPLEVEL_LANG ?= verilog

WPWD=$(shell sh -c 'pwd -W')
PWD=$(shell pwd)
POWLIB=$(PWD)/../..
COCOTB=$(POWLIB)/cocotb/
SIM=icarus
CUSTOM_SIM_DEPS = $(shell find $(POWLIB)/sim/ -name "*.py")

$(info [$(CUSTOM_SIM_DEPS)])

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(POWLIB)/sim/powlib;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(POWLIB)/sim/powlib:$(PYTHONPATH)
endif

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(POWLIB)/hdl/*.v $(PWD)/test_flipflop.v
    COMPILE_ARGS = -g 2001 -I $(POWLIB)/hdl/
    TOPLEVEL = test_flipflop
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

MODULE=test_flipflop

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

