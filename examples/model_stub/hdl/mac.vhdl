-- This file is public domain, it can be freely copied without restrictions.
-- SPDX-License-Identifier: CC0-1.0

-- Multiply-accumulate unit.
-- Every cycle in which `in_valid` is set, `a * b` is added to `acc`
-- two clock cycles later.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- The multiplier has not been implemented yet.
-- Only its interface is defined, and its output is driven by a Python model
-- in the testbench (see tests/test_mac.py).
entity multiplier is
    generic (
        WIDTH : positive := 8
    );
    port (
        a : in  std_logic_vector(WIDTH-1 downto 0);
        b : in  std_logic_vector(WIDTH-1 downto 0);
        p : out std_logic_vector(2*WIDTH-1 downto 0)
    );
end entity multiplier;

architecture stub of multiplier is
begin
end architecture stub;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity mac is
    generic (
        WIDTH     : positive := 8;
        ACC_WIDTH : positive := 32
    );
    port (
        clk      : in  std_logic;
        rst      : in  std_logic;
        in_valid : in  std_logic;
        a        : in  std_logic_vector(WIDTH-1 downto 0);
        b        : in  std_logic_vector(WIDTH-1 downto 0);
        acc      : out std_logic_vector(ACC_WIDTH-1 downto 0)
    );
end entity mac;

architecture rtl of mac is
    signal a_q     : std_logic_vector(WIDTH-1 downto 0);
    signal b_q     : std_logic_vector(WIDTH-1 downto 0);
    signal valid_q : std_logic;
    signal product : std_logic_vector(2*WIDTH-1 downto 0);
    signal acc_q   : unsigned(ACC_WIDTH-1 downto 0);
begin

    i_multiplier : entity work.multiplier
        generic map (
            WIDTH => WIDTH
        )
        port map (
            a => a_q,
            b => b_q,
            p => product
        );

    process (clk) is
    begin
        if rising_edge(clk) then
            if rst = '1' then
                a_q     <= (others => '0');
                b_q     <= (others => '0');
                valid_q <= '0';
                acc_q   <= (others => '0');
            else
                a_q     <= a;
                b_q     <= b;
                valid_q <= in_valid;
                if valid_q = '1' then
                    acc_q <= acc_q + resize(unsigned(product), ACC_WIDTH);
                end if;
            end if;
        end if;
    end process;

    acc <= std_logic_vector(acc_q);

end architecture rtl;
