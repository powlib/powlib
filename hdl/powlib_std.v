`timescale 1ns / 1ps

module powlib_std(

    );
endmodule

module powlib_flipflop(d,q,clk,rst,vld);

  parameter integer         W    = 16;    // Width
  parameter reg     [W-1:0] INIT = 0;    // Initial value
  parameter reg             EAR  = 0;    // Enable asynchronous reset
  parameter reg             EVLD = 0;    // Enable valid
  input     wire    [W-1:0] d;           // Input data
  input     wire            vld;         // Valid  
  input     wire            clk;         // Clock
  input     wire            rst;         // Reset
  output    reg     [W-1:0] q    = INIT; // Output data
  
            wire            vld0 = vld==1 || EVLD==0;

  if (EAR==0) begin
    always @(posedge clk) begin
      if (rst==1) begin
        q <= INIT;
      end else if (vld0==1) begin
        q <= d;
      end
    end
  end else begin
    always @(posedge clk or negedge rst) begin
      if (rst==1) begin
      q <= INIT;
    end else if (vld0==1) begin
      q <= d;
    end    
    end  
  end

endmodule
