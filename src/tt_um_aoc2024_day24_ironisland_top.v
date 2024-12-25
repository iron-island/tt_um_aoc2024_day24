/*
 * Copyright (c) 2024 iron-island
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// TODO: Add .f file instead to be read in testbench and OpenLANE setup
`include "./adventofcode_inputs_submodule/2024/ripple_carry_adder_45b.v"

module tt_um_aoc2024_day24_ironisland_top(
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    reg  [44:0]   x;
    reg  [44:0]   y;
    
    reg  [2:0]    curr_state;
    reg  [2:0]    next_state;

    reg  [7:0]    curr_out;
    reg  [7:0]    next_out;

    wire          enable_output;
    wire [45:0]   z;

    // TT: All output pins must be assigned. If not used, assign to 0.
    assign uo_out = curr_out;
    assign uio_out = 0;
    assign uio_oe  = 0;

    // TT: List all unused inputs to prevent warnings
    wire _unused = &{ena, uio_in, ui_in[7]};

    assign enable_output = ui_in[6];

    always@(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            x <= 45'd0;
            y <= 45'd0;

            curr_state <= 3'd0;

            curr_out <= 8'd0;
        end else if (!enable_output) begin
            x <= {x[41:0], ui_in[2:0]};
            y <= {y[41:0], ui_in[5:3]};
        end else begin
            curr_state <= next_state;

            curr_out <= next_out;
        end
    end

    always@(*) begin
        case (curr_state)
            3'd0    : begin next_state = 3'd1; next_out = z[ 7: 0]; end
            3'd1    : begin next_state = 3'd2; next_out = z[15: 8]; end
            3'd2    : begin next_state = 3'd3; next_out = z[23:16]; end
            3'd3    : begin next_state = 3'd4; next_out = z[31:24]; end
            3'd4    : begin next_state = 3'd5; next_out = z[39:32]; end
            3'd5    : begin next_state = 3'd0; next_out = {2'd0, z[45:40]}; end
            default : begin
                next_state = curr_state;
                next_out   = 8'd0;
            end
        endcase
    end

    ripple_carry_adder_45b u_adder(
        .x(x),
        .y(y),
        .z(z)
    );

endmodule
