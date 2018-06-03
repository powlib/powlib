`include "powlib_std.vh"
`timescale 1ns / 1ps

module powlib_sfifo(wrdata,wrvld,wrrdy,rddata,rdvld,rdrdy,clk,rst);

  parameter  integer            W = 16;
  parameter  integer            D = 8;
  parameter  integer            B = 0;
  input      wire               clk;
  input      wire               rst;
  input      wire    [W-1:0]    wrdata;
  input      wire               wrvld;
  output     wire               wrrdy;
  output     wire    [W-1:0]    rddata;
  output     wire               rdvld;
  input      wire               rdrdy;
  
  localparam integer            WPTR =  powlib_clogb2(D);
  
             wire    [WPTR-1:0] wrptr, rdptr, rdptrm1;      
             
  assign                        wrrdy = wrptr!=rdptrm1;
             wire               wrinc = wrvld && wrrdy; 
             wire               wrclr = (wrptr==(D-1)) && wrinc;    
             
  assign                        rdvld = rdptr!=wrptr;
             wire               rdinc = rdvld && rdrdy;    
             wire               rdclr = (rdptr==(D-1)) && rdinc;                
  
  powlib_cntr     #(.W(WPTR),.ELD(0))             wrcntr_inst  (.cntr(wrptr),.adv(wrinc),.clr(wrclr),.clk(clk),.rst(rst));
  powlib_cntr     #(.W(WPTR),.ELD(0))             rdcntr_inst  (.cntr(rdptr),.adv(rdinc),.clr(rdclr),.clk(clk),.rst(rst));
  powlib_flipflop #(.W(WPTR),.INIT(D-1),.EVLD(1)) rdptrm1_inst (.d(rdptr),.q(rdptrm1),.clk(clk),.rst(rst),.vld(rdinc));
  
  powlib_spram    #(.W(W),.D(D))                  ram_inst     (.wridx(wrptr),.wrdata(wrdata),.wrvld(wrinc),.rdidx(rdptr),.rddata(rddata),.clk(clk));
  
endmodule

module powlib_afifo();
endmodule
