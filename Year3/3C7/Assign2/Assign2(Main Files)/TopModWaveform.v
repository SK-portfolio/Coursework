module TopMod(           
  //input	CCLK, speedup,               
  input clk, rst_n, sh_en,
  output wire detected,
  output wire [3:0] an,
  output wire [7:0] sseg,
  output max_tick_reg, MSB,
  output [21:0]	out,
  output [10:0] counter,msb_out
    );
    reg [31:0] clkscale;
    wire [3:0] d3, d2, d1, d0;
    wire [21:0]	Q_out; 
    wire [10:0]ctr;
    wire speed, max_tick;
    assign MSB = Q_out[21];
    assign max_tick_reg = max_tick;
    assign out = Q_out;
    assign counter = ctr;
 
     //wire clk; // Clock output from clock module

/*
always @* begin 	
if	(speedup) begin
      clkscale = 5000000;
end
else
      clkscale = 20000000;
end
    // instantiate clock module
    clock clock_inst (.CCLK(CCLK), .clkscale(clkscale), .clk(clk));    
*/
 
 //fsm module                                                                     
FSM fsm(                                                                         
  .clk(clk) ,.rst_n(rst_n), .lfsr_output(Q_out[21]), .CW_detected(detected), .max_tick_reg(max_tick), .counter(ctr)
  );  
   
   //LFSR module, output gets passed to FSM  
 LFSR_22bit #(.seed(22'b0001011001001110011111)) lfsr22(.clk(clk), .sh_en(sh_en), .rst_n(rst_n), .Q_out(Q_out), .max_tick_reg(max_tick)
    );
   
   //LFSR module to show every msb in lfsr sequence as it gets updated, output on board LEDs
 MSB_lfsr_Board msb_lfsr(
        .clk(clk), .sh_en(sh_en), .rst_n(rst_n), .MSB(Q_out[21]), .MSB_out(msb_out)
        ); 
        
  disp_hex_mux Display_Count (
            .clk(clk), .reset(1'b0), .hex3(d3), .hex2(d2), .hex1(d1), .hex0(d0), .dp_in(4'b1111), .an(an), .sseg(sseg)
  );
  
  Ctr_SSeg DectoHex (
        .clk(clk), .reset(rst_n), .max_tick(max_tick), .in(detected), .d3(d3), .d2(d2), .d1(d1), .d0(d0)
        );
 
endmodule       