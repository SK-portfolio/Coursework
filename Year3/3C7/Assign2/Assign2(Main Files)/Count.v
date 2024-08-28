module Ctr_SSeg(
    input wire clk, reset, in, max_tick, // Input ports
    output wire [3:0] d3, d2, d1, d0    // Output ports
    );
    reg [3:0] d3_curr, d2_curr, d1_curr, d0_curr; // Registers to store current values
    reg [3:0] d3_next, d2_next, d1_next, d0_next; // Registers to store next values
    
   always @(posedge clk)
    begin
       d3_curr <= d3_next;          // Update with next value
       d2_curr <= d2_next;          // Update with next value
       d1_curr <= d1_next;          // Update with next value
       d0_curr <= d0_next;          // Update with next value
    end
    
   always @*
    begin
       d0_next = d0_curr;          // Set next value as current
       d1_next = d1_curr;          // Set next value as current
       d2_next = d2_curr;          // Set next value as current
       d3_next = d3_curr;          // Set next value as current
       
       if (max_tick)               // If max_tick is true, reset all counters to 0
          begin
             d0_next = 4'b0;
             d1_next = 4'b0;
             d2_next = 4'b0;
             d3_next = 4'b0;
          end
          
        // If input signal is high, increment counters          
       else if (in)
          if (d0_curr != 9)
             d0_next = d0_curr + 1;
          else
             begin
                d0_next = 4'b0;
                if (d1_curr != 9)
                   d1_next = d1_curr + 1;
                else
                   begin
                      d1_next = 4'b0;
                      if (d2_curr != 9)
                         d2_next = d2_curr + 1;
                      else
                         begin
                             d2_next = 4'b0;
                             if(d3_curr != 9)
                                 d3_next = d3_curr + 1;
                             else 
                                 d3_next = 4'b0;
                         end
                   end
             end
    end
 
    // output current values
    assign d0 = d0_curr;
    assign d1 = d1_curr;
    assign d2 = d2_curr;
    assign d3 = d3_curr;
    
endmodule