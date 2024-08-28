`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05.03.2024 13:25:35
// Design Name: 
// Module Name: GrEq2_tb
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


module GrEq2_tb(
   // signal declaration
   reg  [1:0] test_in0, test_in1;
   wire  test_out;

   // instantiate the circuit under test
   geq2 uut
      (.a(test_in0), .b(test_in1), .ageqb(test_out));

   //  test vector generator
   initial
   begin
    $display ("time e0 e1 ageqb"); 
    $monitor ("%d %b % b %b" , 
        $time, test_in0 , test_in1 , test_out);
      // test vector 1
      test_in0 = 2'b00;
      test_in1 = 2'b00;
      # 200;
      // test vector 2
      test_in0 = 2'b01;
      test_in1 = 2'b00;
      # 200;
      // test vector 3
      test_in0 = 2'b01;
      test_in1 = 2'b11;
      # 200;
      // test vector 4
      test_in0 = 2'b10;
      test_in1 = 2'b10;
      # 200;
      // test vector 5
      test_in0 = 2'b10;
      test_in1 = 2'b00;
      # 200;
      // test vector 6
      test_in0 = 2'b11;
      test_in1 = 2'b11;
      # 200;
      // test vector 7
      test_in0 = 2'b11;
      test_in1 = 2'b01;
      # 200;
      // stop simulation

     $stop;
   end
    );
endmodule
