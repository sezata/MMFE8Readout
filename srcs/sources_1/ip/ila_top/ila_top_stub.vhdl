-- Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2014.4.1 (win64) Build 1149489 Thu Feb 19 16:20:35 MST 2015
-- Date        : Mon Feb 01 13:20:30 2016
-- Host        : phys-pc458-4 running 64-bit Service Pack 1  (build 7601)
-- Command     : write_vhdl -force -mode synth_stub
--               C:/Users/kjohns/Documents/X-4b2h/X-4.srcs/sources_1/ip/ila_top/ila_top_stub.vhdl
-- Design      : ila_top
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7a200tfbg484-2
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ila_top is
  Port ( 
    clk : in STD_LOGIC;
    probe0 : in STD_LOGIC_VECTOR ( 31 downto 0 );
    probe1 : in STD_LOGIC_VECTOR ( 7 downto 0 );
    probe2 : in STD_LOGIC_VECTOR ( 7 downto 0 );
    probe3 : in STD_LOGIC_VECTOR ( 15 downto 0 );
    probe4 : in STD_LOGIC_VECTOR ( 7 downto 0 );
    probe5 : in STD_LOGIC_VECTOR ( 7 downto 0 );
    probe6 : in STD_LOGIC_VECTOR ( 7 downto 0 );
    probe7 : in STD_LOGIC_VECTOR ( 7 downto 0 );
    probe8 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe9 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe10 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe11 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe12 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe13 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe14 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe15 : in STD_LOGIC_VECTOR ( 37 downto 0 );
    probe16 : in STD_LOGIC_VECTOR ( 31 downto 0 );
    probe17 : in STD_LOGIC_VECTOR ( 31 downto 0 );
    probe18 : in STD_LOGIC_VECTOR ( 31 downto 0 );
    probe19 : in STD_LOGIC_VECTOR ( 31 downto 0 )
  );

end ila_top;

architecture stub of ila_top is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "clk,probe0[31:0],probe1[7:0],probe2[7:0],probe3[15:0],probe4[7:0],probe5[7:0],probe6[7:0],probe7[7:0],probe8[37:0],probe9[37:0],probe10[37:0],probe11[37:0],probe12[37:0],probe13[37:0],probe14[37:0],probe15[37:0],probe16[31:0],probe17[31:0],probe18[31:0],probe19[31:0]";
attribute x_core_info : string;
attribute x_core_info of stub : architecture is "ila,Vivado 2014.4.1";
begin
end;
