`timescale 1ns / 1ps

module test_afifo();

  localparam W    = 16;
  localparam D    = 8;
  localparam EDBG = 0;
  
  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(3, dut);
  end  
  
  powlib_afifo #(.W(W),.D(D),.EDBG(EDBG)) dut ();

endmodule