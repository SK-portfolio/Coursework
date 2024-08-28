module FXN(
    input [5:0] A, B, minA, minB, AplusB, AminusB, f_XNOR,      // 6-bit input signals for each arithmetic operation
    input AlessB,                                               // 1-bit input signal for A < B value
    input [2:0] fxn,                                            // 3-bit input signal to select operation
    output reg [5:0] X                                          // 6-bit output signal
);
    always @ (*) begin
        case(fxn)                       // switch operation case depending on 3-bit value specified
            3'b000: X = A;              // case0: X (output) equal to input A
            3'b001: X = B;              // case1: X equal to input B
            3'b010: X = minA;           // case2: X equal to minus A (-A)
            3'b011: X = minB;           // case3: X equal to minus B (-B)
            3'b100: X = {5'd0, AlessB}; // case4: X equal to A less than B (lsb set to value of AlessB [1 -> A<B true][0 -> A<B false] all other bits set to 0)
            3'b101: X = f_XNOR;         // case5: X equal to XNOR of inputs(A XNOR B)
            3'b110: X = AplusB;         // case6: X equal to sum of inputs (A + B)
            3'b111: X = AminusB;        // case7: X equal to difference of inputs (A - B)
        endcase
    end
endmodule
