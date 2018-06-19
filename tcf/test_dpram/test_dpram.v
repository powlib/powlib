`timescale 1ns / 1ps

module test_dpram();

  localparam              W = 32;
  localparam              D = 4;
  localparam [W*D-1:0] INIT = {32'h0FED,32'hCBA9,32'h5678,32'h1234}; // Initialize the memory

  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, dut0);
    $dumpvars(2, dut1);
  end  

  powlib_dpram #(.W(W),.D(D),.INIT(INIT),.EWBE(0)) dut0 ();
  powlib_dpram #(.W(W),.D(D),.INIT(INIT),.EWBE(1)) dut1 ();         

endmodule