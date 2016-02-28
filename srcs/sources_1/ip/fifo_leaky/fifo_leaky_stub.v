// Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2014.4 (lin64) Build 1071353 Tue Nov 18 16:47:07 MST 2014
// Date        : Sat Feb 27 17:59:10 2016
// Host        : lppcwks02.physics.harvard.edu running 64-bit CentOS release 6.7 (Final)
// Command     : write_verilog -force -mode synth_stub
//               /home/mmfe8/Desktop/versioning/test_mmfe8/X-4.srcs/sources_1/ip/fifo_leaky/fifo_leaky_stub.v
// Design      : fifo_leaky
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a200tfbg484-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
(* x_core_info = "fifo_generator_v12_0,Vivado 2014.4.1" *)
module fifo_leaky(rst, wr_clk, rd_clk, din, wr_en, rd_en, dout, full, almost_full, empty, almost_empty, rd_data_count, wr_data_count)
/* synthesis syn_black_box black_box_pad_pin="rst,wr_clk,rd_clk,din[31:0],wr_en,rd_en,dout[31:0],full,almost_full,empty,almost_empty,rd_data_count[9:0],wr_data_count[9:0]" */;
  input rst;
  input wr_clk;
  input rd_clk;
  input [31:0]din;
  input wr_en;
  input rd_en;
  output [31:0]dout;
  output full;
  output almost_full;
  output empty;
  output almost_empty;
  output [9:0]rd_data_count;
  output [9:0]wr_data_count;
endmodule
