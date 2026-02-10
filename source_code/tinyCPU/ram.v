module ram(clk, load, addr, d, q);
 parameter DWIDTH=16,AWIDTH=12,WORDS=4096;

 input clk,load;
 input[AWIDTH-1:0] addr;
 input[DWIDTH-1:0] d;
 output[DWIDTH-1:0] q;
 reg [DWIDTH-1:0] q;
 reg [DWIDTH-1:0] mem [WORDS-1:0];

 always @(posedge clk)
   begin
     if(load) mem[addr] <= d;
     q <= mem[addr];
   end

 integer i;
 initial begin
    for(i=0;i<WORDS;i=i+1)
       mem[i]=0;
    mem[12'b000000000000] = 16'b0001000000000000 ;
    mem[12'b000000000001] = 16'b0011000000001110 ;
    mem[12'b000000000010] = 16'b0010000000001110 ;
    mem[12'b000000000011] = 16'b0001000000001010 ;
    mem[12'b000000000100] = 16'b1111000000001111 ;
    mem[12'b000000000101] = 16'b0101000000001101 ;
    mem[12'b000000000110] = 16'b0010000000001110 ;
    mem[12'b000000000111] = 16'b0001000000000001 ;
    mem[12'b000000001000] = 16'b1111000000000000 ;
    mem[12'b000000001001] = 16'b0011000000001110 ;
    mem[12'b000000001010] = 16'b0010000000001110 ;
    mem[12'b000000001011] = 16'b1110000000000000 ;
    mem[12'b000000001100] = 16'b0100000000000010 ;
    mem[12'b000000001101] = 16'b0000000000000000 ;
    mem[12'b000000001110] = 16'b0000000000000000 ;
// Write memory initialization here (e.g., mem[12'h001]=16'h1234;).
 end



endmodule