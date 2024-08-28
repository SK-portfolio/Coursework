module bit8GTEQ(
    input  wire[7:0] c, d,	                 // 8-bit input vectors which represent A and B respectively		
    output wire	GTEQ	                     // single bit output
   );
   wire e0, e1, e2, e3, g0, g1, g2, g3;      //e->equal | g->greater
   
   // bits 0-3 of 2-bit greater-than modules compare four sets of bits from 8-bit c and d
   bit2GT gr_bit0 (.a(c[1:0]), .b(d[1:0]), .AgrB(g0)); //set 1 (bit 1 to 2)
   bit2GT gr_bit1 (.AgrB(g1), .a(c[3:2]), .b(d[3:2])); //set 2 (bit 3 to 4)
   bit2GT gr_bit2 (.AgrB(g2), .a(c[5:4]), .b(d[5:4])); //set 3 (bit 5 to 6)
   bit2GT gr_bit3 (.AgrB(g3), .a(c[7:6]), .b(d[7:6])); //set 4 (bit 7 to 8)
   
   assign GT = g3 | e3 & g2 | e3 & e2 & g1 | e3 & e2 & e1 & g0;    // calculate greater-than result for 8-bit comparison
         
   // bits 0-3 of 2-bit equal-to modules compare four sets of bits from 8-bit c and d
   eq2 eq_bit0 (.a(c[1:0]), .b(d[1:0]), .aeqb(e0)); //set 1 (bit 1 to 2)
   eq2 eq_bit1 (.aeqb(e1), .a(c[3:2]), .b(d[3:2])); //set 2 (bit 3 to 4)
   eq2 eq_bit2 (.aeqb(e2), .a(c[5:4]), .b(d[5:4])); //set 3 (bit 5 to 6)
   eq2 eq_bit3 (.aeqb(e3), .a(c[7:6]), .b(d[7:6])); //set 4 (bit 7 to 8)
   
   assign EQ = e3 & e2 & e1 & e0;      // calculate equal-to result for 8-bit comparison

   assign GTEQ = EQ | GT;       // output final result [1 = c greater than or equal to d] [0 = c less than d]
   
endmodule