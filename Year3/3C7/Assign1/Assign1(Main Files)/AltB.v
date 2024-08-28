module AltB(
    input [5:0]a,b,     // 6-bit input operands a and b
    output wire A_lt_B  // output shows if A less than B [1 = A<B true][0 = A<B false]
);
   wire [7:0] A, B;     // 8-bit A and B values to get greater/equal value from
   wire A_gteq_B;       // greater/equal module
   
     assign A = a[5] ? {2'b11, a} : {2'b00, a};   // convert 6-bit input a to 8-bit A, adding sign extension 11 or 00 depending on if msb of a is 1 or 0
     assign B = b[5] ? {2'b11, b} : {2'b00, b};   // convert 6-bit input b to 8-bit B, adding sign extension 11 or 00 depending on if msb of b is 1 or 0

 bit8GTEQ I_bit8GTEQ(.c(A),.d(B),.GTEQ(A_gteq_B));  // 8-bit greater-than-or-equal-to module
 
    assign A_lt_B = ~A_gteq_B;  // invert greater/equal value to get the less than value 
endmodule