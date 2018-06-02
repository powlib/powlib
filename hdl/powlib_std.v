`timescale 1ns / 1ps

module powlib_flipflop(d,q,clk,rst,vld);

  parameter integer         W    = 1;    // Width
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

module powlib_ffsync(d,q,aclk,bclk,arst,brst,vld);

  parameter integer         W    = 16;    // Width
  parameter reg     [W-1:0] INIT = 0;    // Initial value
  parameter reg             EAR  = 0;    // Enable asynchronous reset
  parameter reg             EVLD = 0;    // Enable valid
  parameter integer         S    = 2;    // Number of B clk domain stages
  input     wire    [W-1:0] d;           // Input data
  input     wire            vld;         // Valid  
  input     wire            aclk, bclk;  // Clock
  input     wire            arst, brst;  // Reset
  output    wire    [W-1:0] q;           // Output data  
  
            genvar          i;
            wire    [W-1:0] ds [0:S];
            wire    [W-1:0] aq;
  
  powlib_flipflop #(.W(W),.INIT(INIT),.EAR(EAR),.EVLD(EVLD))  aff (.d(d),.q(aq),.clk(aclk),.rst(arst),.vld(vld));
  
  for (i=0; i<S; i=i+1) begin
    powlib_flipflop #(.W(W),.INIT(INIT),.EAR(EAR))  bffs (.d(ds[i]),.q(ds[i+1]),.clk(bclk),.rst(brst));
  end
  
  if (S<1) begin
    assign q     = aq;
  end else begin
    assign ds[0] = aq;
    assign q     = ds[S];
  end 
  
endmodule
