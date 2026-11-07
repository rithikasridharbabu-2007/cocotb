# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
"""Test a design in which one submodule is replaced by a Python model.

The ``mac`` design instantiates a ``multiplier`` that has not been implemented yet:
its HDL only defines the ports.
:func:`multiplier_model` stands in for it by watching the multiplier's inputs and
driving its output, so the rest of the design can be tested already.
Once the multiplier is implemented, remove the model and run the same tests.
"""

from __future__ import annotations

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.handle import HierarchyObject
from cocotb.triggers import First, RisingEdge
from cocotb.types import LogicArray
from cocotb_tools.runner import get_runner


async def multiplier_model(multiplier: HierarchyObject) -> None:
    """Behave like a combinational multiplier: ``p = a * b``.

    Recompute the output whenever an input changes.
    """
    while True:
        a = multiplier.a.value
        b = multiplier.b.value
        if a.is_resolvable and b.is_resolvable:
            multiplier.p.value = a.to_unsigned() * b.to_unsigned()
        else:
            # Propagate unknown inputs like real hardware would
            multiplier.p.value = LogicArray("X" * len(multiplier.p))
        await First(multiplier.a.value_change, multiplier.b.value_change)


async def reset(dut) -> None:
    dut.rst.value = 1
    dut.in_valid.value = 0
    dut.a.value = 0
    dut.b.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0


@cocotb.test()
async def mac_accumulates_products(dut):
    """Feed random operands and compare the accumulator against a reference."""
    # Start the model of the unimplemented submodule before anything else.
    cocotb.start_soon(multiplier_model(dut.i_multiplier))
    Clock(dut.clk, 10, unit="ns").start()
    await reset(dut)

    width = len(dut.a)
    acc_mask = (1 << len(dut.acc)) - 1
    expected = 0

    for _ in range(100):
        a = random.randrange(2**width)
        b = random.randrange(2**width)
        valid = random.random() < 0.8

        dut.a.value = a
        dut.b.value = b
        dut.in_valid.value = valid
        await RisingEdge(dut.clk)

        if valid:
            expected = (expected + a * b) & acc_mask

    dut.in_valid.value = 0

    # The product is added two clock cycles after the operands are applied.
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    assert dut.acc.value == expected


@cocotb.test()
async def mac_ignores_invalid_inputs(dut):
    """Operands presented without ``in_valid`` must not change the accumulator."""
    cocotb.start_soon(multiplier_model(dut.i_multiplier))
    Clock(dut.clk, 10, unit="ns").start()
    await reset(dut)

    dut.a.value = 0xFF
    dut.b.value = 0xFF
    dut.in_valid.value = 0
    for _ in range(5):
        await RisingEdge(dut.clk)

    assert dut.acc.value == 0


def test_model_stub_runner():
    """Simulate the model_stub example using the Python runner.

    This file can be run directly or via pytest discovery.
    """
    hdl_toplevel_lang = os.getenv("TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    build_args = []
    if hdl_toplevel_lang == "verilog":
        sources = [proj_path / "hdl" / "mac.sv"]
    elif hdl_toplevel_lang == "vhdl":
        sources = [proj_path / "hdl" / "mac.vhdl"]
        if sim in ["ius", "xcelium"]:
            build_args = ["-v93"]
    else:
        raise ValueError(
            f"A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG={hdl_toplevel_lang}"
        )

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="mac",
        always=True,
        build_args=build_args,
    )
    runner.test(
        hdl_toplevel="mac",
        hdl_toplevel_lang=hdl_toplevel_lang,
        test_module="test_mac",
    )


if __name__ == "__main__":
    test_model_stub_runner()
