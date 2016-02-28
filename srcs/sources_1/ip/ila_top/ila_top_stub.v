// Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2014.4.1 (win64) Build 1149489 Thu Feb 19 16:20:35 MST 2015
// Date        : Mon Feb 01 13:20:30 2016
// Host        : phys-pc458-4 running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode synth_stub
//               C:/Users/kjohns/Documents/X-4b2h/X-4.srcs/sources_1/ip/ila_top/ila_top_stub.v
// Design      : ila_top
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a200tfbg484-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
(* x_core_info = "ila,Vivado 2014.4.1" *)
module ila_top(clk, probe0, probe1, probe2, probe3, probe4, probe5, probe6, probe7, probe8, probe9, probe10, probe11, probe12, probe13, probe14, probe15, probe16, probe17, probe18, probe19)
/* synthesis syn_black_box black_box_pad_pin="clk,probe0[31:0],probe1[7:0],probe2[7:0],probe3[15:0],probe4[7:0],probe5[7:0],probe6[7:0],probe7[7:0],probe8[37:0],probe9[37:0],probe10[37:0],probe11[37:0],probe12[37:0],probe13[37:0],probe14[37:0],probe15[37:0],probe16[31:0],probe17[31:0],probe18[31:0],probe19[31:0]" */;
  input clk;
  input [31:0]probe0;
  input [7:0]probe1;
  input [7:0]probe2;
  input [15:0]probe3;
  input [7:0]probe4;
  input [7:0]probe5;
  input [7:0]probe6;
  input [7:0]probe7;
  input [37:0]probe8;
  input [37:0]probe9;
  input [37:0]probe10;
  input [37:0]probe11;
  input [37:0]probe12;
  input [37:0]probe13;
  input [37:0]probe14;
  input [37:0]probe15;
  input [31:0]probe16;
  input [31:0]probe17;
  input [31:0]probe18;
  input [31:0]probe19;
endmodule
