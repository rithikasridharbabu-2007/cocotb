*************
More Examples
*************

.. note::

    Make sure to use the example code from the tag that matches the version of cocotb installed
    in your environment.

Adder
=====

The directory :file:`examples/adder/` contains an ``adder`` :term:`RTL` in both Verilog and VHDL,
an ``adder_model`` implemented in Python,
and the cocotb testbench with two defined tests — a simple :func:`adder_basic_test` and
a slightly more advanced :func:`adder_randomised_test`.

Python Model in Place of Unimplemented HDL
==========================================

The directory :file:`examples/model_stub/` contains a multiply-accumulate unit ``mac``
in both Verilog and VHDL.
It instantiates a ``multiplier`` that has not been implemented yet:
its :term:`HDL` only declares the ports.

The testbench starts a Python coroutine, ``multiplier_model``, that watches the multiplier's inputs
and drives its output with the product whenever an input changes.
This way the rest of the design can be verified before every part of it exists.
Once the multiplier is implemented, removing the model is all that's needed
to run the same tests against the real :term:`RTL`.

.. literalinclude:: ../../examples/model_stub/tests/test_mac.py
   :language: python
   :pyobject: multiplier_model
