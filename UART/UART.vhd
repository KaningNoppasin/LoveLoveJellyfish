library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
entity UART is
  port (
    CLK      : in std_logic; -- 50 MHz system clock
    NRST     : in std_logic; -- Active-low asynchronous reset
    ADC_CSN  : out std_logic; -- ADC SPI chip-select
    ADC_SCLK : out std_logic; -- ADC SPI SCLK
    ADC_MOSI : out std_logic; -- ADC SPI MOSI
    ADC_MISO : in std_logic;  -- ADC SPI MISO
    LEDS     : out std_logic_vector(7 downto 0); -- 8-bit ADC OUTPUT
    UART_TX  : out std_logic -- UART Transmit Pin
  );
end UART;


architecture behavioral of UART is

  constant SPI_CLK_DIV    : integer := 25;
  constant DATA_WIDTH     : integer := 16; -- for ADC128S022
  constant UART_BAUD_DIV  : integer := 434; -- For 115200 baud with 50 MHz clock

  type state_type is (ST_IDLE, ST_START, ST_SCK_H, ST_SCK_L, ST_WAIT);
  signal state : state_type := ST_IDLE;

  signal cs_n : std_logic := '1';
  signal sclk : std_logic := '0';
  signal mosi : std_logic := '0';

  signal bit_index : integer range 0 to DATA_WIDTH - 1 := 0;
  signal adc_data  : std_logic_vector(11 downto 0)  := (others => '0');
  signal channel   : std_logic_vector(2 downto 0)   := "000";

  signal shift_en  : std_logic := '0';
  signal shift_reg : std_logic_vector(DATA_WIDTH - 1 downto 0);

  constant WAIT_CNT_MAX : integer := 31;
  signal wait_cnt       : integer := 0;

  -- UART signals
  signal uart_baud_count : integer range 0 to UART_BAUD_DIV - 1 := 0;
  signal uart_start_trigger : std_logic := '0'; -- Trigger signal for UART
  signal uart_tx_reg     : std_logic_vector(11 downto 0) := (others => '0');
  signal uart_tx_busy    : std_logic := '0';
  signal uart_tx_bit     : integer range 0 to 11 := 0;

begin

  adc_csn  <= cs_n;
  adc_sclk <= sclk;
  adc_mosi <= mosi;

  -- LED Display Logic
  process (adc_data)
    variable leds_on : integer range 0 to 7;
    variable value   : integer range 0 to 255;
  begin
    --value   := to_integer(unsigned(adc_data(11 downto 4)));
    --value   := value / 32;
    --leds_on := value;
    LEDS <= (others => '0');
    --LEDS(leds_on downto 0) <= (others => '1');
	 LEDS(7 downto 0) <= (adc_data(11 downto 4));
  end process;

  -- SPI clock divider
  process (CLK, NRST)
    variable count : integer range 0 to SPI_CLK_DIV - 1 := 0;
  begin
    if NRST = '0' then
      count := 0;
      shift_en <= '0';
    elsif rising_edge(CLK) then
      if count = SPI_CLK_DIV - 1 then
        count := 0;
        shift_en <= '1';
      else
        count := count + 1;
        shift_en <= '0';
      end if;
    end if;
  end process;

  -- SPI State Machine and UART Trigger
  process (CLK, NRST)
  begin
    if NRST = '0' then
      cs_n      <= '1';
      mosi      <= '0';
      sclk      <= '0';
      adc_data  <= (others => '0');
      channel   <= (others => '0');
      bit_index <= 0;
      wait_cnt  <= 0;
      uart_start_trigger <= '0';

    elsif rising_edge(CLK) then
      case state is
        when ST_IDLE =>
          bit_index <= 0;
          channel   <= "001"; -- Select channel ADC_IN1
          cs_n      <= '1';
          sclk      <= '1';
          state     <= ST_START;

        when ST_START  =>
          shift_reg  <= (others => '0');
          shift_reg(13 downto 11) <= channel; -- for ADC128S022
          cs_n   <= '0';
          state  <= ST_SCK_L;

        when ST_SCK_L =>
          if shift_en = '1' then
            sclk  <= '0';
            mosi  <= shift_reg(shift_reg'left);
            state <= ST_SCK_H;
          end if;

        when ST_SCK_H =>
          if shift_en = '1' then
            sclk      <= '1';
            shift_reg <= shift_reg(shift_reg'left - 1 downto 0) & adc_miso;
            if bit_index = DATA_WIDTH - 1 then
              cs_n     <= '1';
              wait_cnt <= WAIT_CNT_MAX;
              state    <= ST_WAIT;
            else
              bit_index <= bit_index + 1;
              state     <= ST_SCK_L;
            end if;
          end if;

        when ST_WAIT =>
          adc_data <= shift_reg(11 downto 0);
          if wait_cnt = 0 then
            uart_start_trigger <= '1'; -- Set trigger for UART process
            uart_tx_reg <= shift_reg(11 downto 0); -- Load ADC data into UART register
            state <= ST_IDLE;
          else
            wait_cnt <= wait_cnt - 1;
          end if;

        when others =>
          state <= ST_IDLE;
      end case;
    end if;
  end process;

  -- UART transmission process
  process (CLK, NRST)
  begin
    if NRST = '0' then
      UART_TX <= '1'; -- Idle state for UART line
      uart_tx_busy <= '0';
      uart_tx_bit <= 0;
--      uart_start_trigger <= '0';

    elsif rising_edge(CLK) then
      if uart_start_trigger = '1' and uart_tx_busy = '0' then
        uart_tx_busy <= '1';
        uart_tx_bit <= 0;
        UART_TX <= '0'; -- Start bit
--        uart_start_trigger <= '0'; -- Clear trigger after starting transmission
      elsif uart_tx_busy = '1' then
        uart_baud_count <= uart_baud_count + 1;
        if uart_baud_count = UART_BAUD_DIV - 1 then
          uart_baud_count <= 0;
          if uart_tx_bit < 12 then
            UART_TX <= uart_tx_reg(uart_tx_bit);
            uart_tx_bit <= uart_tx_bit + 1;
          else
            UART_TX <= '1'; -- Stop bit
            uart_tx_busy <= '0';
          end if;
        end if;
      end if;
    end if;
  end process;

end behavioral;
