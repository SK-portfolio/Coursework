// Basys Board and Spartan-3E Starter Board
// LED Bar Graph Test bargraphtest.v
// c 2008 Embedded Design using Programmable Gate Arrays  Dennis Silage


module bargraphtest(input CCLK, sw0, sw1, sw2, sw3, sw4, sw5, sw6, sw7, output LD7, LD6, LD5, LD4,
                    LD3, LD2, LD1, LD0);

wire [7:0] data;
						  
clock M0 (CCLK, 625000, clock);
bargraph M1 (clock, sw0, sw1, sw2, sw3, sw4, sw5, sw6, sw7, LD7, LD6, LD5, LD4,
             LD3, LD2, LD1, LD0); 
gendata M2 (clock, data);

endmodule

// generate bar graph test data

module gendata(input clock, output reg [7:0] gdata);

always@(negedge clock)
	gdata=gdata+1;
	
endmodule
