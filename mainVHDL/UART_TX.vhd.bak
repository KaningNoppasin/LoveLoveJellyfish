library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity signalProj is
    port (
        clk      : in std_logic;  -- Assuming 50MHz input clock
        reset_n  : in std_logic;
        led      : out std_logic_vector(9 downto 0);
        tx       : out std_logic
    );
end entity;

architecture rtl of signalProj is
    -- ADC component declaration remains the same
    component adc0 is
        port (
            CLOCK : in  std_logic;
            RESET : in  std_logic;
            CH0   : out std_logic_vector(11 downto 0);
            CH1   : out std_logic_vector(11 downto 0);
            CH2   : out std_logic_vector(11 downto 0);
            CH3   : out std_logic_vector(11 downto 0);
            CH4   : out std_logic_vector(11 downto 0);
            CH5   : out std_logic_vector(11 downto 0);
            CH6   : out std_logic_vector(11 downto 0);
            CH7   : out std_logic_vector(11 downto 0)
        );
    end component;

    -- Sampling rate constants
    -- For 4kHz sampling rate with 50MHz clock: 50MHz/44.1kHz = 12500
    constant SAMPLE_RATE_DIVIDER : integer := 1134;
  
    
    -- Sampling control signals
    signal sample_timer : integer range 0 to SAMPLE_RATE_DIVIDER-1 := 0;
    signal sample_tick : std_logic := '0';
    
    -- UART constants (for 2M baud with 50MHz clock)
    constant CLKS_PER_BIT : integer := 25;
    
    -- Existing signals
    signal adc_value : std_logic_vector(11 downto 0);
    signal led_reg   : std_logic_vector(9 downto 0);
    signal adc_sum   : unsigned(15 downto 0);
    signal sample_count : unsigned(7 downto 0);
    signal adc_avg   : unsigned(11 downto 0);
    signal amplified_value : unsigned(11 downto 0);
    
    -- UART signals
    type uart_state_type is (IDLE, START_BIT, DATA_BITS, STOP_BIT);
    signal uart_state : uart_state_type := IDLE;
    signal clk_count : integer range 0 to CLKS_PER_BIT-1 := 0;
    signal bit_index : integer range 0 to 7 := 0;
    signal tx_data   : std_logic_vector(7 downto 0) := (others => '0');
    signal uart_send_trigger : std_logic := '0';
    signal byte_select : integer range 0 to 1 := 0;

begin
    -- ADC instance
    u0 : adc0
        port map (
            CLOCK => clk,
            RESET => '0',
            CH0   => adc_value,
            CH1   => open,
            CH2   => open,
            CH3   => open,
            CH4   => open,
            CH5   => open,
            CH6   => open,
            CH7   => open
        );

    -- Sample rate generator process
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            sample_timer <= 0;
            sample_tick <= '0';
        elsif rising_edge(clk) then
            sample_tick <= '0';  -- Default state
            
            if sample_timer = SAMPLE_RATE_DIVIDER-1 then
                sample_timer <= 0;
                sample_tick <= '1';  -- Generate sampling pulse
            else
                sample_timer <= sample_timer + 1;
            end if;
        end if;
    end process;

    -- Main ADC processing
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            led_reg <= (others => '0');
            adc_sum <= (others => '0');
            sample_count <= (others => '0');
            adc_avg <= (others => '0');
            uart_send_trigger <= '0';
        elsif rising_edge(clk) then
            uart_send_trigger <= '0';  -- Default state
            
            if sample_tick = '1' then  -- Only process on sample tick
                -- Send current ADC value directly
                amplified_value <= unsigned(adc_value);  -- Or apply any needed amplification
                uart_send_trigger <= '1';  -- Trigger UART transmission
                
                -- Update LED display based on amplitude
                if unsigned(adc_value) >= x"A00" then
                    led_reg <= "1111111111";
                elsif unsigned(adc_value) >= x"900" then
                    led_reg <= "0111111111";
                elsif unsigned(adc_value) >= x"800" then
                    led_reg <= "0011111111";
                elsif unsigned(adc_value) >= x"700" then
                    led_reg <= "0001111111";
                elsif unsigned(adc_value) >= x"600" then
                    led_reg <= "0000111111";
                elsif unsigned(adc_value) >= x"500" then
                    led_reg <= "0000011111";
                elsif unsigned(adc_value) >= x"400" then
                    led_reg <= "0000001111";
                elsif unsigned(adc_value) >= x"300" then
                    led_reg <= "0000000111";
                elsif unsigned(adc_value) >= x"200" then
                    led_reg <= "0000000011";
                elsif unsigned(adc_value) >= x"100" then
                    led_reg <= "0000000001";
                else
                    led_reg <= "0000000000";
                end if;
            end if;
        end if;
    end process;

    -- UART transmission process (remains largely the same)
    process(clk)
    begin
        if rising_edge(clk) then
            case uart_state is
                when IDLE =>
                    tx <= '1';
                    if uart_send_trigger = '1' then
                        if byte_select = 0 then
                            tx_data <= std_logic_vector(amplified_value(11 downto 4));
                        else
                            tx_data <= std_logic_vector(amplified_value(3 downto 0)) & "0000";
                        end if;
                        uart_state <= START_BIT;
                        clk_count <= 0;
                    end if;

                when START_BIT =>
                    tx <= '0';
                    if clk_count = CLKS_PER_BIT-1 then
                        clk_count <= 0;
                        uart_state <= DATA_BITS;
                        bit_index <= 0;
                    else
                        clk_count <= clk_count + 1;
                    end if;

                when DATA_BITS =>
                    tx <= tx_data(bit_index);
                    if clk_count = CLKS_PER_BIT-1 then
                        clk_count <= 0;
                        if bit_index = 7 then
                            uart_state <= STOP_BIT;
                        else
                            bit_index <= bit_index + 1;
                        end if;
                    else
                        clk_count <= clk_count + 1;
                    end if;

                when STOP_BIT =>
                    tx <= '1';
                    if clk_count = CLKS_PER_BIT-1 then
                        clk_count <= 0;
                        uart_state <= IDLE;
                        if byte_select = 0 then
                            byte_select <= 1;
                        else
                            byte_select <= 0;
                        end if;
                    else
                        clk_count <= clk_count + 1;
                    end if;
            end case;
        end if;
    end process;

    led <= led_reg;
    
end architecture;