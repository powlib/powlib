`timescale 1ns / 1ps

module test_pipe(d,q,clk,rst,vld);

  parameter              W    = 8;    // Width
  parameter      [W-1:0] INIT = 0;    // Initial value
  parameter              EAR  = 0;    // Enable asynchronous reset
  parameter              EVLD = 1;    // Enable valid
  parameter              S    = 8;    // Number of stages
  input     wire [W-1:0] d;           // Input data
  output    wire [W-1:0] q;           // Output data
  input     wire         clk;         // Clock
  input     wire         rst;         // Reset
  input     wire         vld;         // Valid

  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, dut);
  end  

  powlib_pipe #(.W(W),.INIT(INIT),.EAR(EAR),.EVLD(EVLD),.S(S)) dut (.d(d),.q(q),.clk(clk),.rst(rst),.vld(vld));               
    
endmodule
