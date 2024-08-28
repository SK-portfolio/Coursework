module FSM(
  input	clk, rst_n,           // Clock and reset signals
  input lfsr_output,          // Output from LFSR (Linear Feedback Shift Register)
  output CW_detected,         // Output indicating whether the codeword is detected
  input max_tick_reg,         // Maximum tick register
  output reg [10:0] counter   // Counter for codeword detection
);

  reg [3:0] curr_state, nxt_state;  // Current and next states for the FSM

//Codeword -> 11111010101 

localparam IDLE = 4'b0000;    // Reset state 
localparam   S1  = 4'b0001;   // 1 is detected 
localparam   S2  = 4'b0010;   // 11 is detected 
localparam   S3  = 4'b0011;   // 111 is detected 
localparam   S4  = 4'b0100;   // 1111 is detected 
localparam   S5  = 4'b0101;   // 11111 is detected
localparam   S6  = 4'b0110;   // 111110 is detected
localparam   S7  = 4'b0111;   // 1111101 is detected
localparam   S8 = 4'b1000;    // 11111010 is detected
localparam   S9  = 4'b1001;   // 111110101 is detected
localparam   S10  = 4'b1010;  // 1111101010 is detected
localparam   S11 = 4'b1011;   // 11111010101 is detected

assign    CW_detected = (curr_state == S11) ? 1'b1 : 1'b0;  // set to 1 if curr_state is s11, else set to 0

always @ (posedge clk) begin   //rising edge sensitive 
if(!rst_n) begin
		 curr_state	<=	IDLE; 
		 counter ='d0;
		 end
		 
		 else begin 
	  
		    curr_state <= nxt_state;
   if (nxt_state == S11) 
   begin
   counter <= counter +1;
   end 
 
     if (max_tick_reg) 
     counter <='d0;
   
end

end


always @ (*) begin 
case (curr_state)

IDLE : begin 
        if (lfsr_output) // 1
          nxt_state = S1;
         else 
           nxt_state  = IDLE;
       end 
 
 S1 : begin 
        if (lfsr_output) //1
          nxt_state  = S2;
         else 
           nxt_state  = IDLE;
       end 
S2 : begin 
        if (lfsr_output) //1
          nxt_state  = S3;
         else 
           nxt_state  = S1;
       end 
 S3 : begin 
        if (lfsr_output) // 1
          nxt_state  = S4;
         else 
           nxt_state  = S1;
       end 
 S4 : begin 
        if (lfsr_output) //1
          nxt_state  = S5;
         else 
           nxt_state  = S1;
       end 
 S5 : begin 
        if (lfsr_output) //1
          nxt_state  = S6;
         else 
           nxt_state  = IDLE;
       end 
 S6 : begin 
        if (!lfsr_output) //0
          nxt_state  = S7;
         else 
           nxt_state  =IDLE;
       end 
 S7 : begin 
        if (lfsr_output) //1
          nxt_state  = S8;
         else 
           nxt_state  = S3;
       end 
 S8 : begin 
        if (!lfsr_output)//0
          nxt_state  = S9;
         else 
           nxt_state  =S1;
       end 
 S9 : begin 
        if (lfsr_output) //1
          nxt_state  = S10;
         else 
           nxt_state  =S1;
       end 
 S10 : begin 
        if (!lfsr_output) //0
          nxt_state  = S11;
         else 
           nxt_state = S5;
       end
 S11 : begin 
        if (lfsr_output) //1
          nxt_state  = S1;      // Sequence found, return to checking first digit
         else 
          nxt_state  = IDLE;    // Sequence not found, return to waiting for first digit
       end 
default: 
         nxt_state = IDLE;

          
endcase
end

endmodule