`timescale 1ns / 1ps

module test_gray();

`include "powlib_std.vh"

  localparam                       W        = 5;
  localparam                       X        = 1;
  localparam                       INIT     = 0;
                                   
             wire [W-1:0]          cntr; 
             wire [W-1:0]          encoded;
             wire [W-1:0]          decoded;
             wire                  adv;
             wire                  clr;
             wire                  clk;
             wire                  rst;
             
  
  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, cntr_inst);
    $dumpvars(2, encode_inst);
    $dumpvars(2, decode_inst);
  end  

  powlib_cntr #(.W(W),.X(X),.INIT(INIT)) cntr_inst (
    .cntr(cntr),.adv(adv),.clr(clr),
    .clk(clk),.rst(rst));
    
  powlib_grayencodeff #(.W(W),.INIT(INIT)) encode_inst (
    .d(cntr),.q(encoded),
    .clk(clk),.rst(rst));
    
  powlib_graydecodeff #(.W(W),.INIT(powlib_grayencode(INIT))) decode_inst (
    .d(encoded),.q(decoded),
    .clk(clk),.rst(rst));

endmodule