// Basys Board and Spartan-3E Starter Board
// LED Bar Graph bargraph.v
// c 2007 Embedded System Design in Verilog
//           using Programmable Gate Arrays  Dennis Silage

module bargraph(input clock, sw0, sw1, sw2, sw3, sw4, sw5, sw6, sw7,
           output LD7, LD6, LD5, LD4, LD3, LD2, LD1, LD0);

	reg [7:0] leddata;		// LED data
	
assign LD7=leddata[7];
assign LD6=leddata[6];
assign LD5=leddata[5];
assign LD4=leddata[4];
assign LD3=leddata[3];
assign LD2=leddata[2];
assign LD1=leddata[1];
assign LD0=leddata[0];

always@(posedge clock)
	 begin
		leddata=8'b00000000;
		if (sw0==1)
			leddata[0]=8'b00000001;
		if (sw1==1)
			leddata[1]=8'b00000011;
		if (sw2==1)
			leddata[2]=8'b00000111;
		if (sw3==1)
			leddata[3]=8'b00001111;
		if (sw4==1)
			leddata[4]=8'b00011111;
		if (sw5==1)
			leddata[5]=8'b00111111;
		if (sw6==1)
			leddata[6]=8'b01111111;
		if (sw7==1)
			leddata[7]=8'b11111111;
	end
		
endmodule
