// Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2014.4.1 (win64) Build 1149489 Thu Feb 19 16:23:09 MST 2015
// Date        : Tue Sep 22 14:20:28 2015
// Host        : PHYS-PC452-2 running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode synth_stub
//               c:/AzPjcts/Xproj/NSW-MM/new_mmfe8/mmfe8_xadc_V8_Leaky-v14p4_9-9-15/X-2/X-2.srcs/sources_1/ip/ila_ext_trig/ila_ext_trig_stub.v
// Design      : ila_ext_trig
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a200tfbg484-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
(* x_core_info = "ila,Vivado 2014.4.1" *)
module ila_ext_trig(clk, probe0, probe1, probe2, probe3, probe4, probe5)
/* synthesis syn_black_box black_box_pad_pin="clk,probe0[3:0],probe1[11:0],probe2[11:0],probe3[11:0],probe4[15:0],probe5[15:0]" */;
  input clk;
  input [3:0]probe0;
  input [11:0]probe1;
  input [11:0]probe2;
  input [11:0]probe3;
  input [15:0]probe4;
  input [15:0]probe5;
endmodule
