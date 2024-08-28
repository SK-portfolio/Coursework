module SB_2sComp(
    input [5:0] X,      // 6-bit two's complement input
    output [5:0] Y      // 6-bit two's complement output
);

    wire [5:0]invX;     // wire to store 1's complement of X
    assign  invX = ~X;  // Assign invese of X to 'invX' wire
  
   // 6-bit ripple carry adder where 1 is added to lsb of 1's comp X to get 2's complement as Y
   SB_ripple_adder I_adder (.x(invX),.y(6'b000001),.sel(1'b0),.c_out(),.overflow(),.sum(Y));    
endmodule
 