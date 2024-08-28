library ieee;
    use ieee.std_logic_1164.all;
    use ieee.std_logic_arith.all;
    use ieee.std_logic_textio.all;
    use ieee.std_logic_unsigned.all;
    use work.modulator_pkg.all;
library unisim;
    use unisim.vcomponents.all;
entity modulator is
    generic(
    -- User defined settings for the pwm design
    design_setting_g : design_setting_t_rec := design_setting_c
    );
    port(
        clk_in              : in std_logic;                     -- input clock signal
        sw0                 : in std_logic;                     -- signal made for selecting frequency
        div_factor_freqhigh : in std_logic_vector(31 downto 0); -- input clock division when sw0 = '1'
        div_factor_freqlow  : in std_logic_vector(31 downto 0); -- input clock division when sw0 = '0'
        pwm_out             : out std_logic                     -- pulse width modulated signal
        );
end entity;
architecture rtl of modulator is
-- amplitude counter
signal ampl_cnt_s  : std_logic_vector(design_setting_g.depth-1 downto 0);
-- current amplitude value of the sine signal
signal sine_ampl_s : std_logic_vector(design_setting_g.width-1 downto 0); 
-- signal which frequency depends on the sw0 state
signal freq_trig_s : std_logic := '0';
begin
freq_ce : entity work.frequency_trigger(rtl)    -- frequency trigger module instance
    port map(
        clk_in              => clk_in,
        sw0                 => sw0,
        div_factor_freqhigh => div_factor_freqhigh,
        div_factor_freqlow  => div_factor_freqlow,
        freq_trig           => freq_trig_s
        );
counterampl : entity work.counter(rtl)          -- counter module instance
    generic map(
        cnt_value_g => design_setting_g.cntampl_value,
        depth_g     => design_setting_g.depth
        )
    port map (
        clk_in  => clk_in,
        cnt_en  => freq_trig_s,
        cnt_out => ampl_cnt_s
        );
sine : entity work.sine(rtl)                    -- digital sine module instance
    generic map(
        depth_g => design_setting_g.depth,
        width_g => design_setting_g.width
        )
    port map(
        ampl_cnt => ampl_cnt_s,
        clk_in   => clk_in,
        sine_out => sine_ampl_s
        );
pwmmodule : entity work.pwm (rtl)               -- pwm module instance
    generic map (
        width_g => design_setting_g.width
        )
    port map (
        clk_in              => clk_in,
        sw0                 => sw0,
        sine_ampl           => sine_ampl_s,
        div_factor_freqhigh => conv_std_logic_vector(conv_integer(div_factor_freqhigh)/(2**design_setting_g.width), 32),
        div_factor_freqlow  => conv_std_logic_vector(conv_integer(div_factor_freqlow)/(2**design_setting_g.width), 32),
        pwm_out             => pwm_out
        );
end;