# Default to verilog
TOPLEVEL_LANG ?= verilog

WPWD=$(shell sh -c 'pwd -W')
PWD=$(shell pwd)
POWLIB=$(PWD)/../..
COCOTB=$(POWLIB)/cocotb/
SIM=icarus

$(info [$(CUSTOM_SIM_DEPS)])

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(POWLIB)/sim;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(POWLIB)/sim:$(PYTHONPATH)
endif

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(POWLIB)/hdl/*.v $(PWD)/test_dpram.v
    COMPILE_ARGS = -g 2001 -I $(POWLIB)/hdl/     
    TOPLEVEL = test_dpram
else
    $(error "A valid value (verilog) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

MODULE=test_dpram

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

