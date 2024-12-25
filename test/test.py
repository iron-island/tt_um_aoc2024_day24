# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

from collections import defaultdict

def and_gate(x, y):
    return x & y

def or_gate(x, y):
    return x | y

def xor_gate(x, y):
    return x ^ y

def process_inputs(in_file):
    output = 0

    wires_dict = defaultdict(int)
    gates_dict = defaultdict(tuple)
    with open(in_file) as file:
        line = file.readline()
    
        get_gates = False
        while line:
            line = line.strip()

            if (line == ""):
                get_gates = True
            elif not (get_gates):
                wire, init = line.split(": ")
                wires_dict[wire] = int(init)
            else:
                operation, outwire = line.split(" -> ")
                x, op, y = operation.split(" ")
                if (op == "AND"):
                    op = and_gate
                elif (op == "OR"):
                    op = or_gate
                elif (op == "XOR"):
                    op = xor_gate
                gates_dict[outwire] = (x, op, y)

            line = file.readline()

    # Process x and y as decimal
    init_x = 0
    init_y = 0
    for bit in range(44, -1, -1):
        x_wire = "x" + f'{bit:02d}'
        y_wire = "y" + f'{bit:02d}'

        assert(x_wire in wires_dict)
        assert(y_wire in wires_dict)

        init_x += wires_dict[x_wire]*(2**bit)
        init_y += wires_dict[y_wire]*(2**bit)

    # Simulate
    while True:
        val_changed = False
        for wire in gates_dict:
            x, op, y = gates_dict[wire]

            x_val = wires_dict[x]
            y_val = wires_dict[y]
            new_val = op(x_val, y_val)
            old_val = wires_dict[wire]

            if (new_val != old_val):
                wires_dict[wire] = new_val
                val_changed = True

        if not (val_changed):
            break

    # Evaluate
    output = 0
    for wire in gates_dict:
        if ("z" in wire) and wires_dict[wire]:
            bit = int(wire[1:])
            output += 2**bit

    return init_x, init_y, output

@cocotb.test()
async def test_project(dut):
    init_x, init_y, output = process_inputs("../src/adventofcode_inputs_submodule/2024/input24.txt")
    print(f'Initial x[44:0] = {init_x}')
    print(f'Initial y[44:0] = {init_y}')
    print(f'Expected z[45:0] = {output}')

    dut._log.info("Start")

    # Set the clock period to 1 us (1 MHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    for i in range(14, -1, -1):
        x_in_bits = ((init_x >> i*3) & 7)
        y_in_bits = ((init_y >> i*3) & 7)

        dut.ui_in.value = x_in_bits + (y_in_bits << 3)

        await ClockCycles(dut.clk, 1)
    dut.ui_in.value = x_in_bits + (y_in_bits << 3) + (1 << 6)

    # TODO: assertion for output
    await ClockCycles(dut.clk, 8)
