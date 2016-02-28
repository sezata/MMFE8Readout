-- Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2014.4 (lin64) Build 1071353 Tue Nov 18 16:47:07 MST 2014
-- Date        : Sat Feb 27 18:00:38 2016
-- Host        : lppcwks02.physics.harvard.edu running 64-bit CentOS release 6.7 (Final)
-- Command     : write_vhdl -force -mode synth_stub
--               /home/mmfe8/Desktop/versioning/test_mmfe8/X-4.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0_stub.vhdl
-- Design      : clk_wiz_0
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7a200tfbg484-2
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity clk_wiz_0 is
  Port ( 
    clk_in1 : in STD_LOGIC;
    clk_200_o : out STD_LOGIC;
    clk_160_o : out STD_LOGIC;
    clk_100_o : out STD_LOGIC;
    clk_50_o : out STD_LOGIC;
    clk_40_o : out STD_LOGIC;
    clk_20_o : out STD_LOGIC;
    clk_10_o : out STD_LOGIC
  );

end clk_wiz_0;

architecture stub of clk_wiz_0 is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "clk_in1,clk_200_o,clk_160_o,clk_100_o,clk_50_o,clk_40_o,clk_20_o,clk_10_o";
begin
end;
