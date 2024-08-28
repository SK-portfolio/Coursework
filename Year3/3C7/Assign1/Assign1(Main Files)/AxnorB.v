module AxnorB(
    input [5:0] A, B,   // 6-bit input operands A and B
    output [5:0] X      // 6-bit output result X
  );
    assign X= A~^B;     // assign X to result of A NOT OR B (A XNOR B)
endmodule
