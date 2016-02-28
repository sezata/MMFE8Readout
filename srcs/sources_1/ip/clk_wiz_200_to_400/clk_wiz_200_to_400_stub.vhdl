-- Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2014.4 (lin64) Build 1071353 Tue Nov 18 16:47:07 MST 2014
-- Date        : Sat Feb 27 18:01:06 2016
-- Host        : lppcwks02.physics.harvard.edu running 64-bit CentOS release 6.7 (Final)
-- Command     : write_vhdl -force -mode synth_stub
--               /home/mmfe8/Desktop/versioning/test_mmfe8/X-4.srcs/sources_1/ip/clk_wiz_200_to_400/clk_wiz_200_to_400_stub.vhdl
-- Design      : clk_wiz_200_to_400
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7a200tfbg484-2
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity clk_wiz_200_to_400 is
  Port ( 
    clk_in1_p : in STD_LOGIC;
    clk_in1_n : in STD_LOGIC;
    clk_out_400 : out STD_LOGIC
  );

end clk_wiz_200_to_400;

architecture stub of clk_wiz_200_to_400 is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "clk_in1_p,clk_in1_n,clk_out_400";
begin
end;
