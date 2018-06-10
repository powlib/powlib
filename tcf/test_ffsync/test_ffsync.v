`timescale 1ns / 1ps

module test_ffsync(d,q,aclk,bclk,arst,brst,vld);

  parameter                W    = 8;    // Width
  parameter        [W-1:0] INIT = 0;    // Initial value
  parameter                EAR  = 0;    // Enable asynchronous reset
  parameter                EVLD = 0;    // Enable valid
  parameter                S    = 3;    // Number of B clk domain stages
  input     wire   [W-1:0] d;           // Input data
  input     wire           vld;         // Valid  
  input     wire           aclk, bclk;  // Clock
  input     wire           arst, brst;  // Reset
  output    wire   [W-1:0] q;           // Output data  

  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, dut);
  end

  powlib_ffsync #(.W(W),.INIT(INIT),.EAR(EAR),.EVLD(EVLD),.S(S)) dut (.d(d),.q(q),.aclk(aclk),.bclk(bclk),
                                                                      .arst(arst),.brst(brst),.vld(vld));               
    
endmodule
