# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(PWD)/../hdl/mac.sv
else ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(PWD)/../hdl/mac.vhdl
    ifneq ($(filter $(SIM),ius xcelium),)
        COMPILE_ARGS += -v93
    endif
else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

COCOTB_TOPLEVEL     := mac
COCOTB_TEST_MODULES := test_mac

include $(shell cocotb-config --makefiles)/Makefile.sim
