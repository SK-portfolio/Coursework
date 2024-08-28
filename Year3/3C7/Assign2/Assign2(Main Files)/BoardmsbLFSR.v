module MSB_lfsr_Board(
    input clk, rst_n, sh_en, MSB,                // sigle bit inputs
    output reg [10:0] MSB_out                // show each msb in sequence on board (hopefully)
);  
    //reg MSB;
    //reg max_tick_reg, MSB;
    reg [10:0] MSB_state, MSB_next;     // 11-bit register for current&next MSB vals
    
    always @ (posedge clk) begin
        if (!rst_n) begin
            MSB_state <= 11'b0;
            MSB_next <= 11'b0;

            MSB_state[0] = MSB;
		 end
		 else if(sh_en) begin
		 	         
			   MSB_next = {MSB_state[9:0],MSB};
               MSB_state = MSB_next;                 
         end
        MSB_out <= MSB_state;
    end   
endmodule
