// Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2014.4 (lin64) Build 1071353 Tue Nov 18 16:47:07 MST 2014
// Date        : Sat Feb 27 18:01:05 2016
// Host        : lppcwks02.physics.harvard.edu running 64-bit CentOS release 6.7 (Final)
// Command     : write_verilog -force -mode synth_stub
//               /home/mmfe8/Desktop/versioning/test_mmfe8/X-4.srcs/sources_1/ip/clk_wiz_200_to_400/clk_wiz_200_to_400_stub.v
// Design      : clk_wiz_200_to_400
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a200tfbg484-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module clk_wiz_200_to_400(clk_in1_p, clk_in1_n, clk_out_400)
/* synthesis syn_black_box black_box_pad_pin="clk_in1_p,clk_in1_n,clk_out_400" */;
  input clk_in1_p;
  input clk_in1_n;
  output clk_out_400;
endmodule
