module TopMod(
  input	CCLK, speedup, rst_n, sh_en,                   // Input ports
  output wire detected,                                 // Output for codeword detection
  output wire [3:0] an,                                 // Anode control signals for 7-segment display
  output wire [7:0] sseg,                               // 7-segment display output
  output max_tick_reg,                                  // Output indicating maximum tick
  //output [21:0]	out,                               // 22LFSR output
  //output [10:0] counter,                             //Counter(for Waveform)
  output [10:0] msb_out                                // Output for MSB stream
);

    wire clk;                                           // Clock output from clock module
    reg [31:0] clkscale;                                // Register for clock scale
    wire speed;                                         // Input to toggle speed clkscale size
    wire [3:0] d3, d2, d1, d0;                          // Individual digit outputs for display
    wire [21:0] Q_out;                                  // Output from LFSR module
    wire max_tick;                                      // Maximum tick indication
    wire [10:0] ctr;                                    // Counter output

    assign max_tick_reg = max_tick;
    assign out = Q_out;
    assign counter = ctr;


// Clock generation based on speedup signal
always @* begin 	
if	(speedup) begin
      clkscale = 5000000;       // Clock scale lower if speedup
end
else
      clkscale = 20000000;     // Else default clock scale
end

    // Instantiate clock module
    clock clock_inst (.CCLK(CCLK), .clkscale(clkscale), .clk(clk));    

 
    // Finite State Machine instantiation - take MSB from 22LFSR output as input                                                                    
FSM fsm(                                                                         
  .clk(clk) ,.rst_n(rst_n), .lfsr_output(Q_out[21]), .CW_detected(detected), .max_tick_reg(max_tick), .counter(ctr)
  );  
   
 // LFSR 22-bit module instantiation
 LFSR_22bit #(.seed(22'b0001011001001110011111)) lfsr22(.clk(clk), .sh_en(sh_en), .rst_n(rst_n), .Q_out(Q_out), .max_tick_reg(max_tick)
    );
   
   //LFSR module to show every msb in lfsr sequence as it gets updated, output on board LEDs
 MSB_lfsr_Board msb_lfsr(
        .clk(clk), .sh_en(sh_en), .rst_n(rst_n), .MSB(Q_out[21]), .MSB_out(msb_out)
        ); 
   // 7-segment display module instantiation   
  disp_hex_mux Display_Count (
            .clk(clk), .reset(1'b0), .hex3(d3), .hex2(d2), .hex1(d1), .hex0(d0), .dp_in(4'b1111), .an(an), .sseg(sseg)
  );
  // Decimal to hexadecimal conversion module instantiation
  Ctr_SSeg DectoHex (
            .clk(clk), .reset(rst_n), .max_tick(max_tick), .in(detected), .d3(d3), .d2(d2), .d1(d1), .d0(d0)
  );
 
endmodule       