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

    # Generate module definition and input, output declarations
    print("module ripple_carry_adder_45b(")
    print("    input wire  [44:0] x,")
    print("    input wire  [44:0] y,")
    print("    output wire [45:0] z")
    print(");")

    # Generate wire declarations for x* and y*
    for wire in wires_dict:
        print(f'    wire {wire};')
    print("")

    # Generate wire declarations
    for wire in gates_dict:
        print(f'    wire {wire};')
    print("")

    # Generate assign statements for rewiring x* and y*
    for wire in wires_dict:
        input_var = wire[0]
        bit = int(wire[1:])
        print(f'    assign {wire} = {input_var}[{bit}];')
    print("")

    # Generate assign statements for rewiring z*
    for wire in gates_dict:
        if (wire[0] == "z"):
            bit = int(wire[1:])
            print(f'    assign z[{bit:>2}] = {wire};')
    print("")

    # Generate assign statements for gates
    for wire in gates_dict:
        x, op, y = gates_dict[wire]

        if (op == and_gate):
            print(f'    assign {wire} = {x} & {y};')
        elif (op == or_gate):
            print(f'    assign {wire} = {x} | {y};')
        elif (op == xor_gate):
            print(f'    assign {wire} = {x} ^ {y};')

    # Generate endmodule
    print("endmodule")

process_inputs("./adventofcode_inputs_submodule/2024/input24.txt")
