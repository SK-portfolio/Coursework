library ieee;
    use ieee.std_logic_1164.all;
    use ieee.std_logic_arith.all;
    use ieee.std_logic_unsigned.all;
library unisim;
    use unisim.vcomponents.all;
    use work.modulator_pkg.all;
    
entity modulator_wrapper is
    generic(
        -- If some module is top, it needs to implement the differential clk buffer,
        -- otherwise this variable will be overwritten by a upper hierarchy layer
        this_module_is_top_g : module_is_top_t := yes;
        -- Parameter that specifies major characteristics of the board that will be used 
        -- to implement the modulator design
        -- Possible choices: """lx9""", """zedboard""", """ml605""", """kc705""", """microzed""", ""socius"""
        -- Adjust the modulator_pkg.vhd file to add more        
        board_name_g : string := """zedboard""";
        -- User defined settings for the pwm design
        design_setting_g : design_setting_t_rec := design_setting_c   
         
        );
    port(
        clk_p   : in std_logic;    -- differential input clock signal
        clk_n   : in std_logic;    -- differential input clock signal
        sw0     : in std_logic;    -- signal made for selecting frequency
        pwm_out : out std_logic    -- pulse width modulated signal
--        clk_en  : out std_logic    -- clock enable port used only for MicroZed board
        );
         
end entity;
architecture rtl of modulator_wrapper is
-- Between architecture and begin is declaration area for types, signals and constants
-- Everything declared here will be visible in the whole architecture
    -- input clock signal
    signal clk_in_s : std_logic;
    -- c1_c = fclk/(2^depth*2^width)                   - c1_c = 95.3674, fclk = 100 MHz
    constant c1_c : real := get_board_info_f(board_name_g).fclk/(real((2**design_setting_g.depth)*(2**design_setting_g.width)));
     -- div_factor_freqhigh_c = (c1_c/f_high)*2^width  - threshold value of frequency a = 110592   
    constant div_factor_freqhigh_c : integer := integer(c1_c/design_setting_g.f_high)*(2**design_setting_g.width);
    -- div_factor_freqlow_c  = (c1_c/f_low)*2^width    - threshold value of frequency b = 389120
    constant div_factor_freqlow_c  : integer := integer(c1_c/design_setting_g.f_low)*(2**design_setting_g.width);
        
begin
    -- in case of MicroZed board we must enable on-board clock generator
--    clk_en <= '1';
    -- if module is top, it has to generate the differential clock buffer in case
    -- of a differential clock, otherwise it will get a single ended clock signal
    -- from the higher hierarchy
    
    clk_buf_if_top : if (this_module_is_top_g = yes) generate
        clk_buf : if (get_board_info_f(board_name_g).has_diff_clk = yes) generate
            ibufgds_inst : ibufgds
                generic map(
                    ibuf_low_pwr => true,
                    -- low power (true) vs. performance (false) setting for referenced I/O standards
                    iostandard => "default"
                )
                port map (
                    o => clk_in_s, -- clock buffer output
                    i => clk_p,    -- diff_p clock buffer input
                    ib => clk_n    -- diff_n clock buffer input
                );
        end generate clk_buf;
        no_clk_buf : if (get_board_info_f(board_name_g).has_diff_clk = no) generate
            clk_in_s <= clk_p;
        end generate no_clk_buf;
        
    end generate clk_buf_if_top;
    not_top : if (this_module_is_top_g = no) generate
        clk_in_s <= clk_p;
    end generate not_top;
    
    pwmmodulator : entity work.modulator   -- modulator module instance
        generic map(
            design_setting_g => design_setting_g
            )
            
        port map(
            clk_in              => clk_in_s,
            sw0                 => sw0,
            div_factor_freqhigh => conv_std_logic_vector(div_factor_freqhigh_c, 32),
            div_factor_freqlow  => conv_std_logic_vector(div_factor_freqlow_c, 32),
            pwm_out             => pwm_out
            );
end;