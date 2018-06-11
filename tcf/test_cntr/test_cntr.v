`timescale 1ns / 1ps

module test_cntr;
  
  parameter              W    = 8;  // Width
  parameter      [W-1:0] X    = 1;  // Increment / decrement value
  parameter      [W-1:0] INIT = 0;  // Initialize value
  parameter              ELD  = 1;  // Enable load feature
  parameter              EAR  = 1;  // Enable asynchronous reset feature

  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, dut0);
    $dumpvars(2, dut1);
  end

  powlib_cntr #(.W(W),.X(1), .INIT(INIT),.ELD(ELD),.EAR(EAR)) dut0 (.cntr(),.nval(),.adv(),.ld(),.clr(),.clk(),.rst());  
  powlib_cntr #(.W(W),.X(-1),.INIT(INIT),.ELD(ELD),.EAR(EAR)) dut1 (.cntr(),.nval(),.adv(),.ld(),.clr(),.clk(),.rst());               
    
endmodule
