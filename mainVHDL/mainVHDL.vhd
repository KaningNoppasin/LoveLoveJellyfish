------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
------------------------------------------------------------------

entity mainVHDL is
  generic ( WIDTH : natural := 8 );
  port(
     CLK  : in std_logic;
     nRST : in std_logic;
     LEDS : out std_logic_vector(WIDTH-1 downto 0)
  );
end mainVHDL;

architecture SYNTH of mainVHDL is
  constant ALL_ONES     : unsigned := to_unsigned(2**WIDTH-1,WIDTH);
  constant COUNT_PERIOD : integer := 10000000;
  subtype count_t is integer range 0 to (COUNT_PERIOD-1); 
  signal  count : count_t := 0;
  signal  reg   : std_logic_vector(WIDTH-1 downto 0);
  signal  shift_en : std_logic;

begin

  LEDS <= not reg; -- used the register's bits (inverted) for LEDs

  process (nRST, CLK) begin
    if nRST = '0' then
      count <= 0;
      shift_en <= '0';
    elsif rising_edge(CLK) then
      -- check whether the counter reaches the max. value.
      if count = (COUNT_PERIOD-1) then 
        count <= 0;       -- reset the counter.
        shift_en <= '1';  -- enable register shift.
      else
        count <= count+1; -- increment counter by 1.
        shift_en <= '0';  -- disable register shift.
      end if;
    end if;
  end process;

  process (nRST, CLK) begin
    if nRST = '0' then
      reg <= (others => '0'); -- clear the shift register.
    elsif rising_edge(CLK) then
      if  shift_en='1' then -- register shifting is enabled.  
        if reg = std_logic_vector( ALL_ONES ) then
          -- clear the shift register.
          reg <= (others => '0'); 
        else
          -- shift left, insert '1' as LSB.
          reg <= reg(reg'left-1 downto 0) & '1'; 
        end if;
        end if;
    end if;
  end process;

end SYNTH;