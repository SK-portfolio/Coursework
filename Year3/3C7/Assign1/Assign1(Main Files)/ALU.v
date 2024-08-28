module ALU(
    input [5:0] A, B,          // 6-bit input operands A and B
    output [5:0] X,            // 6-bit output result X
    input [2:0] fxn            // 3-bit input for operation selection
);
wire [5:0] minus_A, minus_B, PLUS, MINUS, XNOR, LESS; // wires for operation signals
    
SB_2sComp I_minus_A ( .X(A), .Y(minus_A)); // 2's complement module to compute negative A (-A)
SB_2sComp I_minus_B ( .X(B), .Y(minus_B)); // 2's complement module to compute negative B (-B)
  
AltB I_AltB (.A_lt_B(LESS), .a(A), .b(B));  // module to compare A and B (A < B)

AxnorB  I_AxnorB (.A(A), .B(B), .X(XNOR));  // module to derive XNOR of A and B (A XNOR B)
   
SB_ripple_adder I_ADD (.x(A), .y(B), .sel(1'b0), .c_out(),.overflow(), .sum(PLUS));   // ripple adder module for addition (A + B) [sel = 0]
SB_ripple_adder I_SUB (.x(A), .y(B), .sel(1'b1), .c_out(),.overflow(), .sum(MINUS));  // ripple adder module for subtraction (A - B) [sel = 1]
   
FXN I_FXN (.X(X), .A(A), .B(B), .fxn(fxn), .minA(minus_A), .minB(minus_B), 
           .f_XNOR(XNOR), .AminusB(MINUS), .AplusB(PLUS), .AlessB(LESS));   // module to perform selected operation based on chosen 3-bit input value

endmodule
