module ALU_TestBench;
    reg [5:0] A, B; // 6-bit input operands
    reg [2:0] fxn;  // 3-bit input signal to select arithmetic operation 
    wire [5:0] X;   // 6-bit output signal
        
    ALU uut (.A(A), .B(B), .fxn(fxn), .X(X));   // ALU module expressed with IO connections to get all X values
    
    //Test Vectors
    initial
    begin
      // test vec1 - Both positive [Board Number(16)]
      A = 6'b000001;      //1
      B = 6'b000110;      //6 
      fxn = 3'b000;       // X = A
      # 100;
      // test vec2 - Both negative
      A = 6'b111100;    //-4 
      B = 6'b111001;    //-7
      fxn = 3'b001;     // X = B
      # 100;
      // test vec3 - A positive, B negative
      A = 6'b000101;       //5
      B = 6'b110110;       //-10
      fxn = 3'b010;        // X = -A (2's Complement)
      # 100;
      // test vec4 -  A negative, B positive
      A = 6'b101100;       //-20
      B = 6'b010000;       //16
      fxn = 3'b011;        // X = -B (2's Complement)
      # 100;
      // test vec5 - Both positive
      A = 6'b001011;       //11
      B = 6'b010010;       //18
      fxn = 3'b100;        // X = A<B
      # 100;
      // test vec6 - Both negative
      A = 6'b101101;      //-19
      B = 6'b100100;      //-28
      fxn = 3'b101;       // X = A XNOR B
      # 100;
      // test vec7 - A positive, B negative
      A = 6'b001111;    //15
      B = 6'b111001;    //-7
      fxn = 3'b110;     // X = A+B
      # 100;
      // test vec8 - A negative, B positive
	  A = 6'b110111;    //-9
      B = 6'b011110;    //30
      fxn = 3'b111;     // X = A-B
      # 100;
      $stop;
   end
   initial 
   begin
   $display("A, B, fxn, X ");
   $monitor("%d %b %b  %b", $time, A, B, fxn, X); // display A, B, fxn, and X values at each simulation step
   end 
   

endmodule

