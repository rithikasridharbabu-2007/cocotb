// This file is public domain, it can be freely copied without restrictions.
// SPDX-License-Identifier: CC0-1.0

// Multiply-accumulate unit.
// Every cycle in which `in_valid` is set, `a * b` is added to `acc`
// two clock cycles later.

`timescale 1ns/1ps

// The multiplier has not been implemented yet.
// Only its interface is defined, and its output is driven by a Python model
// in the testbench (see tests/test_mac.py).
module multiplier #(
    parameter int WIDTH = 8
) (
    input  logic [WIDTH-1:0]   a,
    input  logic [WIDTH-1:0]   b,
    output logic [2*WIDTH-1:0] p
);
endmodule

module mac #(
    parameter int WIDTH     = 8,
    parameter int ACC_WIDTH = 32
) (
    input  logic                 clk,
    input  logic                 rst,
    input  logic                 in_valid,
    input  logic [WIDTH-1:0]     a,
    input  logic [WIDTH-1:0]     b,
    output logic [ACC_WIDTH-1:0] acc
);

    logic [WIDTH-1:0]   a_q;
    logic [WIDTH-1:0]   b_q;
    logic               valid_q;
    logic [2*WIDTH-1:0] product;

    multiplier #(
        .WIDTH (WIDTH)
    ) i_multiplier (
        .a (a_q),
        .b (b_q),
        .p (product)
    );

    always_ff @(posedge clk) begin
        if (rst) begin
            a_q     <= '0;
            b_q     <= '0;
            valid_q <= 1'b0;
            acc     <= '0;
        end else begin
            a_q     <= a;
            b_q     <= b;
            valid_q <= in_valid;
            if (valid_q) begin
                acc <= acc + ACC_WIDTH'(product);
            end
        end
    end

endmodule
