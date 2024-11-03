LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

ENTITY mainVHDL IS
  PORT (
    CLK : IN STD_LOGIC; -- 50 MHz system clock
    NRST : IN STD_LOGIC; -- Active-low asynchronous reset
    ADC_CSN : OUT STD_LOGIC; -- ADC SPI chip-select
    ADC_SCLK : OUT STD_LOGIC; -- ADC SPI SCLK
    ADC_MOSI : OUT STD_LOGIC; -- ADC SPI MOSI
    ADC_MISO : IN STD_LOGIC; -- ADC SPI MISO
    LEDS : OUT STD_LOGIC_VECTOR(7 DOWNTO 0); -- 8-bit ADC OUTPUT
    tx : OUT STD_LOGIC -- UART
  );
END mainVHDL;

ARCHITECTURE behavioral OF mainVHDL IS
  SIGNAL adc_output : STD_LOGIC_VECTOR(7 DOWNTO 0) := (OTHERS => '0');
BEGIN

  ADC_Controller : entity work.ADC_Controller
    port map(
      CLK => CLK,
      NRST => NRST,
      ADC_CSN => ADC_CSN,
      ADC_SCLK => ADC_SCLK,
      ADC_MOSI => ADC_MOSI,
      ADC_MISO => ADC_MISO,
      LEDS => adc_output
    );

    UART_TX : entity work.UART_TX
      port map(
        clk => CLK,
        reset_n => NRST,
        adcData => adc_output,
        tx => tx
      );

      LEDS <= adc_output;

--  PROCESS (CLK, NRST)
--  END PROCESS;

END behavioral;