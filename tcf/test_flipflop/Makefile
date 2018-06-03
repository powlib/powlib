# Default to verilog
TOPLEVEL_LANG ?= verilog

WPWD=$(shell sh -c 'pwd -W')
PWD=$(shell pwd)
COCOTB=$(PWD)/../../..

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(PWD)/../cosim;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(PWD)/../cosim:$(PYTHONPATH)
endif

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(WPWD)/../hdl/endian_swapper.sv
    TOPLEVEL = endian_swapper_sv
else ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(WPWD)/../hdl/endian_swapper.vhdl
    TOPLEVEL = endian_swapper_vhdl
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

MODULE=test_endian_swapper

CUSTOM_COMPILE_DEPS = hal

LD_LIBRARY_PATH := $(PWD)/../cosim:$(LD_LIBRARY_PATH)

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

.PHONY: hal
hal:
	-cd ../cosim && make

# Stuff below is useful for profiling
# Need grof2dot from https://github.com/jrfonseca/gprof2dot
test_profile.pstat: sim

callgraph.svg: test_profile.pstat
	gprof2dot.py -f pstats $< | dot -Tsvg -o $@

.PHONY: profile
profile:
	COCOTB_ENABLE_PROFILING=1 $(MAKE) callgraph.svg


clean::
	-rm -rf test_profile.pstat
	-rm -rf callgraph.svg
	-cd ../cosim && make clean

