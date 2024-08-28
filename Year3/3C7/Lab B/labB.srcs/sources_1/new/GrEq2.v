`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05.03.2024 13:18:37
// Design Name: 
// Module Name: GrEq2
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
module GrEq2(
    //2 inputs and a wire for each bit (4)
    input wire i0, i1, j0, j1,
    //3 outputs for the 3 different cases
    output wire eq, gt
   );
   
   //wires used for each situation, before entering OR gates
   wire p0, p1, p2, p3, p4, p5, p6;

   assign eq = p0 | p1 | p2 | p3; 
   assign p0 = i0 & ~j0 & i1 & ~j1;
   assign p1 = i0 & j0 & i1 & j1;
   assign p2 = ~i0 & j0 & ~i1 & j1;
   assign p3 = ~i0 & ~j0 & ~i1 & ~j1;
   
   assign gt = p4 | p5 | p6;
   assign p4 = j0 & ~j1;
   assign p5 = i0 & j0 & ~i1;
   assign p6 = i0 & ~i1 & ~j1;
endmodule
