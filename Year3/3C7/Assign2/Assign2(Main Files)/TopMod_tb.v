module TopMod_tb();
reg clk;
wire max_tick_reg;
reg rst_n;
reg sh_en;
wire detected;
wire [21:0] Q_out;
wire [10:0] counter;
wire [10:0] MSB_out;
wire MSB;

TopMod dut(.clk(clk), .rst_n(rst_n), .sh_en(sh_en), .detected(detected)
           ,.max_tick_reg(max_tick_reg)
           ,.out(Q_out), .counter(counter), .MSB(MSB)  //uncomment for waveform
           ,.msb_out(MSB_out)
           );

initial
begin
    sh_en = 1'b1;
   end
  
  initial
begin
    rst_n = 1'b0; //setting reset to low to intialise the seed 
    #4;
    rst_n = 1'b1; //then back to 1 to start LFSR
  
  end

initial begin 
	        clk	= 1'b0;
			forever	#1	clk	=	!clk;
			
			end 



    

endmodule