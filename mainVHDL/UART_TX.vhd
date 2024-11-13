LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

ENTITY UART_TX IS
    PORT (
        clk : IN STD_LOGIC; -- Assuming 50MHz input clock
        reset_n : IN STD_LOGIC;
        uart_send_trigger : IN STD_LOGIC;
        adcData : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
        tx : OUT STD_LOGIC
    );
END ENTITY;

ARCHITECTURE rtl OF UART_TX IS
    -- UART constants (for 2M baud with 50MHz clock)
    CONSTANT CLKS_PER_BIT : INTEGER := 25;
--    CONSTANT CLKS_PER_BIT : INTEGER := 200; -- 250_000

    -- UART signals
    TYPE uart_state_type IS (IDLE, START_BIT, DATA_BITS, STOP_BIT);
    SIGNAL uart_state : uart_state_type := IDLE;
    SIGNAL clk_count : INTEGER RANGE 0 TO CLKS_PER_BIT - 1 := 0;
    SIGNAL bit_index : INTEGER RANGE 0 TO 7 := 0;
    SIGNAL tx_data : STD_LOGIC_VECTOR(7 DOWNTO 0) := (OTHERS => '0');
    -- SIGNAL uart_send_trigger : STD_LOGIC := '0';
    SIGNAL byte_select : INTEGER RANGE 0 TO 1 := 0;

BEGIN
    -- UART transmission process (remains largely the same)
    PROCESS (clk)
    BEGIN
        IF rising_edge(clk) THEN
            CASE uart_state IS
                WHEN IDLE =>
                    tx <= '1';
                    IF uart_send_trigger = '1' THEN
                        tx_data <= adcData;
                        uart_state <= START_BIT;
                        clk_count <= 0;
                    END IF;

                WHEN START_BIT =>
                    tx <= '0';
                    IF clk_count = CLKS_PER_BIT - 1 THEN
                        clk_count <= 0;
                        uart_state <= DATA_BITS;
                        bit_index <= 0;
                    ELSE
                        clk_count <= clk_count + 1;
                    END IF;

                WHEN DATA_BITS =>
                    tx <= tx_data(bit_index);
                    IF clk_count = CLKS_PER_BIT - 1 THEN
                        clk_count <= 0;
                        IF bit_index = 7 THEN
                            uart_state <= STOP_BIT;
                        ELSE
                            bit_index <= bit_index + 1;
                        END IF;
                    ELSE
                        clk_count <= clk_count + 1;
                    END IF;

                WHEN STOP_BIT =>
                    tx <= '1';
                    IF clk_count = CLKS_PER_BIT - 1 THEN
                        clk_count <= 0;
                        uart_state <= IDLE;
                    ELSE
                        clk_count <= clk_count + 1;
                    END IF;
            END CASE;
        END IF;
    END PROCESS;
END ARCHITECTURE;