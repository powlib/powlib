`include "powlib_std.vh"
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

  parameter integer         W    = 1;    // Width
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

module powlib_pipe(d,q,clk,rst,vld);

  parameter integer         W    = 1;    // Width
  parameter reg     [W-1:0] INIT = 0;    // Initial value
  parameter reg             EAR  = 0;    // Enable asynchronous reset
  parameter reg             EVLD = 0;    // Enable valid
  parameter integer         S    = 4;    // Number of stages
  input     wire    [W-1:0] d;           // Input data
  output    wire    [W-1:0] q;           // Output data
  input     wire            clk;         // Clock
  input     wire            rst;         // Reset
  input     wire            vld;         // Valid
  
  if (S<1) begin
    assign q = d;
  end else begin
    powlib_ffsync #(.W(W),.INIT(INIT),.EAR(EAR),.EVLD(EVLD),.S(S-1)) ffs (.d(d),.q(q),.aclk(clk),.bclk(clk),.arst(rst),.brst(rst),.vld(vld));
  end
  
endmodule

module powlib_cntr(cntr,nval,adv,ld,clr,clk,rst);
  
  parameter integer        W    = 32; // Width
  parameter reg    [W-1:0] X    = 1;  // Increment / decrement value
  parameter reg    [W-1:0] INIT = 0;  // Initialize value
  parameter reg            ELD  = 1;  // Enable load feature
  parameter reg            EAR  = 0;  // Enable asynchronous reset feature
  output    wire   [W-1:0] cntr;      // Current counter value
  input     wire   [W-1:0] nval;      // New value
  input     wire           adv;       // Advances the counter
  input     wire           ld;        // Loads a new value into counter
  input     wire           clr;       // Clears the counter to INIT
  input     wire           clk;       // Clock
  input     wire           rst;       // Reset
  
            wire           ld0 = ld && ELD;
  
  powlib_flipflop #(.W(W),.INIT(INIT),.EAR(EAR),.EVLD(1)) cntr_inst (
    .d((clr) ? INIT   : 
       (ld0) ? nval   :
       (adv) ? cntr+X : 0),
    .q(cntr),
    .clk(clk),
    .rst(rst),
    .vld(clr||ld0||adv));
  
endmodule

module powlib_spram(wridx,wrdata,wrvld,rdidx,rddata,clk);

  parameter integer            W    = 16;               // Width
  parameter integer            D    = 8;                // Depth
  parameter reg     [W*D-1:0]  INIT = 0;                // Initializes the memory
  parameter integer            WIDX = powlib_clogb2(D); // Width of index
  input     wire    [WIDX-1:0] wridx;                   // Write index 
  input     wire    [W-1:0]    wrdata;                  // Write data
  input     wire               wrvld;                   // Write data valid
  input     wire    [WIDX-1:0] rdidx;                   // Read index
  output    wire    [W-1:0]    rddata;                  // Read data
  input     wire               clk;                     // Clock
            reg     [W-1:0]    mem[D-1:0];              // Array (i.e. should be inferred as block ram)
            integer            i;      
   
  assign rddata = mem[rdidx]; 
  
  initial begin
    for (i=0; i<D; i=i+1) begin
      mem[i] <= INIT[W*i +: W];
    end    
  end
  
  always @(posedge clk) begin           
    if (wrvld==1) begin
      mem[wridx] <= wrdata;
    end
  end

endmodule
