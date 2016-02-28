// Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2014.4 (lin64) Build 1071353 Tue Nov 18 16:47:07 MST 2014
// Date        : Sat Feb 27 18:00:38 2016
// Host        : lppcwks02.physics.harvard.edu running 64-bit CentOS release 6.7 (Final)
// Command     : write_verilog -force -mode synth_stub
//               /home/mmfe8/Desktop/versioning/test_mmfe8/X-4.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0_stub.v
// Design      : clk_wiz_0
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a200tfbg484-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module clk_wiz_0(clk_in1, clk_200_o, clk_160_o, clk_100_o, clk_50_o, clk_40_o, clk_20_o, clk_10_o)
/* synthesis syn_black_box black_box_pad_pin="clk_in1,clk_200_o,clk_160_o,clk_100_o,clk_50_o,clk_40_o,clk_20_o,clk_10_o" */;
  input clk_in1;
  output clk_200_o;
  output clk_160_o;
  output clk_100_o;
  output clk_50_o;
  output clk_40_o;
  output clk_20_o;
  output clk_10_o;
endmodule
