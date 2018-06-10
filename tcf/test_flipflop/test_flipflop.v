`timescale 1ns / 1ps

module test_flipflop(d,q,clk,rst,vld);
       
  parameter              W    = 8;    // Width
  parameter      [W-1:0] INIT = 0;    // Initial value
  parameter              EAR  = 0;    // Enable asynchronous reset
  parameter              EVLD = 1;    // Enable valid  
  input     wire [W-1:0] d;           // Input data
  input     wire         vld;         // Valid  
  input     wire         clk;         // Clock
  input     wire         rst;         // Reset
  output    wire [W-1:0] q;           // Output data    

  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(1, dut);
  end

  powlib_flipflop #(.W(W),.INIT(INIT),.EAR(EAR),.EVLD(EVLD)) dut (.d(d),.q(q),.clk(clk),.rst(rst),.vld(vld));               
    
endmodule
