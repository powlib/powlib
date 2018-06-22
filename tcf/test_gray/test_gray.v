`timescale 1ns / 1ps

module test_gray();

`include "powlib_std.vh"

  localparam              W    = 4;
  localparam              X    = 1;
  localparam              INIT = 0;
  localparam              EDBG = 1;
  localparam              ID   = "GC";

             wire [W-1:0] cntr; 
             wire [W-1:0] gray;
             wire [W-1:0] decoded;
             wire         adv;
             wire         clr;
             wire         clk;
             wire         rst;
  
  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, dut);
    $dumpvars(2, decode_inst);
  end  

  powlib_graycntr #(.W(W),.X(X),.INIT(INIT),.EDBG(EDBG),.ID(ID)) dut (
    .cntr(cntr),.gray(gray),.adv(adv),.clr(clr),
    .clk(clk),.rst(rst));
    
  powlib_flipflop #(.W(W),.INIT(INIT)) decode_inst ( 
    .d(powlib_graydecode(gray)),
    .q(decoded),
    .clk(clk),.rst(rst));

endmodule