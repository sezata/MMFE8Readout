-- Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2014.4.1 (win64) Build 1149489 Thu Feb 19 16:23:09 MST 2015
-- Date        : Tue Sep 22 14:20:28 2015
-- Host        : PHYS-PC452-2 running 64-bit Service Pack 1  (build 7601)
-- Command     : write_vhdl -force -mode synth_stub
--               c:/AzPjcts/Xproj/NSW-MM/new_mmfe8/mmfe8_xadc_V8_Leaky-v14p4_9-9-15/X-2/X-2.srcs/sources_1/ip/ila_ext_trig/ila_ext_trig_stub.vhdl
-- Design      : ila_ext_trig
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7a200tfbg484-2
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ila_ext_trig is
  Port ( 
    clk : in STD_LOGIC;
    probe0 : in STD_LOGIC_VECTOR ( 3 downto 0 );
    probe1 : in STD_LOGIC_VECTOR ( 11 downto 0 );
    probe2 : in STD_LOGIC_VECTOR ( 11 downto 0 );
    probe3 : in STD_LOGIC_VECTOR ( 11 downto 0 );
    probe4 : in STD_LOGIC_VECTOR ( 15 downto 0 );
    probe5 : in STD_LOGIC_VECTOR ( 15 downto 0 )
  );

end ila_ext_trig;

architecture stub of ila_ext_trig is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "clk,probe0[3:0],probe1[11:0],probe2[11:0],probe3[11:0],probe4[15:0],probe5[15:0]";
attribute x_core_info : string;
attribute x_core_info of stub : architecture is "ila,Vivado 2014.4.1";
begin
end;
