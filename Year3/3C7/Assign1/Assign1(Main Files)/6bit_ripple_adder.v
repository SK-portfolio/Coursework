module SB_ripple_adder(
    input wire [5:0] x, y,                // 6-bit two's complement numbers to add
    input sel,                            // sel -> [0 = add] [1 = sub]
                                        
    output wire overflow,                 // Output flagging overflow in the sum output
               [5:0] sum,                 // 2s complement sum of x and y
                c_out,                    // MSB Carry out from the sum
          wire c1, c2, c3, c4, c5, c6     // carry output for each full adder
    );
    assign overflow = c6 ^ c5 ;           //overflow = c6 xor c5
    
    assign c0 = sel;                     //initialise 1st output as 0

    FullAdder adder_1(.a(x[0]),.b(y[0] ^ sel), .cin(sel), .s(sum[0]), .cout(c1));   // 1st bit
    FullAdder adder_2(.a(x[1]),.b(y[1] ^ sel), .cin(c1), .s(sum[1]), .cout(c2));    // 2nd bit
    FullAdder adder_3(.a(x[2]),.b(y[2] ^ sel), .cin(c2), .s(sum[2]), .cout(c3));    // 3rd bit
    FullAdder adder_4(.a(x[3]),.b(y[3] ^ sel), .cin(c3), .s(sum[3]), .cout(c4));    // 4th bit
    FullAdder adder_5(.a(x[4]),.b(y[4] ^ sel), .cin(c4), .s(sum[4]), .cout(c5));    // 5th bit
    FullAdder adder_6(.a(x[5]),.b(y[5] ^ sel), .cin(c5), .s(sum[5]), .cout(c6));    // 6th bit
    
    assign c_out = c6;                    // declare final carry output as output of ripplr adder
endmodule