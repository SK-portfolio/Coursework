// Listing 1.7
// The `timescale directive specifies that
// the simulation time unit is 1 ns  and
// the simulation timestep is 10 ps
`timescale 1 ns/10 ps

module sbra_testbench;
   // signal declaration
   reg  [5:0] test_in0, test_in1;
   reg select;
   wire [5:0] test_out;
   wire test_overflow;
   wire test_cout;
   // instantiate the circuit under test
   sixbit_ripple_adder uut (.x(test_in0),.y(test_in1),.sum(test_out),.sel(select),.overflow(test_overflow),.c_out(test_cout));
    

   //  test vector generator
   initial
   begin
      //test vector 1
      test_in0 = 6'b010101;
      test_in1 = 6'b101010;
      select = 0;
      #200;
      // test vector 2
      test_in0 = 6'b001100;
      test_in1 = 6'b110111;
      select = 1;
      #200;
      // test vector 3
      test_in0 = -6'b100001;
      test_in1 = 6'b010010;
      select = 0;
      #200;
      //test vector 4
      test_in0 = 6'b111001;
      test_in1 = 6'b100111;
      select = 1;
      #200;
      // test vector 5
      test_in0 = 6'b011011;
      test_in1 = -6'b101101;
      select = 0;
      #200;
      // test vector 6
      test_in0 = 6'b110101;
      test_in1 = 6'b011110;
      select = 1;
      #200; 
      // test vector 7
      test_in0 = 6'b111111;
      test_in1 = 6'b111111;
      select = 0;
      #200;
      // test vector 8
      test_in0 = 6'b000000;
      test_in1 = 6'b000000;
      select = 1;
      #200;
      // test vector 9
      test_in0 = -6'b011010;
      test_in1 = -6'b101011;
      select = 0;
      #200;                      
      // stop simulation
      //$stop;
   end
   

endmodule