module bit2GT(
    input  wire[1:0] a, b,  // 2-bit inputs a and b represents bit8GTEQ c and d rsp.
    output wire AgrB        // output shows if A greater than B
);

   wire [0:2] prod;         // 3 wires for product terms

   
   assign prod[0] = a[1] & ~b[1];             // prod-term0: a[1] AND (NOT b[1])
   assign prod[1] = a[0] & ~b[1] & ~b[0];     // prod-term1: a[0] AND (NOT b[1]) AND (NOT b[0])
   assign prod[2] = a[1] & a[0] & ~b[0];      // prod-term2: a[1] AND a[0] AND (NOT b[0])
 
   assign AgrB = prod[0] | prod[1] | prod[2]; // OR of all product terms to get output

endmodule




