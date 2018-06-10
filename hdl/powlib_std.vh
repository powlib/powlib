

function integer powlib_clogb2;
  input reg [31:0] value;
  begin
    value = value - 1;
    for (powlib_clogb2=0; value>0; powlib_clogb2=powlib_clogb2+1) begin
      value = value >> 1;
    end
  end
endfunction

