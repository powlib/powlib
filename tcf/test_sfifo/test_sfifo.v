`timescale 1ns / 1ps

module test_sfifo();

  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(2, dut);
  end  

  powlib_sfifo #(.W(16),.D(8),.EDBG(1)) dut ();       

endmodule