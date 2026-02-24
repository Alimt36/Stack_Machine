
`define IDLE 3'b000
`define FETCHA 3'b001
`define FETCHB 3'b010
`define EXECA 3'b011
`define EXECB 3'b100

`define ADD 5'b00000
`define SUB 5'b00001
`define MUL 5'b00010
`define SHL 5'b00011
`define SHR 5'b00100
`define BAND 5'b00101
`define BOR 5'b00110
`define BXOR 5'b00111
`define AND 5'b01000
`define OR 5'b01001
`define EQ 5'b01010
`define NE 5'b01011
`define GE 5'b01100
`define LE 5'b01101
`define GT 5'b01110
`define LT 5'b01111
`define NEG 5'b10000
`define BNOT 5'b10001
`define NOT 5'b10010

`define HALT 4'b0000
`define PUSHI 4'b0001
`define PUSH 4'b0010
`define POP 4'b0011
`define JMP 4'b0100
`define JZ 4'b0101
`define JNZ 4'b0110
`define IN 4'b1101
`define OUT 4'b1110
`define OP 4'b1111

//---------------------------------------------------------------------------------------------------------------------------
// indirect addressing support 
//---------------------------------------------------------------------------------------------------------------------------
`define PUSH_IND 4'b0111  
`define POP_IND 4'b1000   

//---------------------------------------------------------------------------------------------------------------------------
// additional state for indirecct sync RAM access 
//---------------------------------------------------------------------------------------------------------------------------
`define EXECC  3'b101


module state(clk,reset,run,cont,halt,cs);
  
  input clk, reset, run, cont, halt;
  output[2:0]cs;

  reg[2:0]cs;

  always @(posedge clk or negedge reset)
    if(!reset) cs <= `IDLE;
    else
      case(cs)
        `IDLE: if(run) cs <= `FETCHA;
        `FETCHA: cs <= `FETCHB;
        `FETCHB: cs <= `EXECA;
        `EXECA: if(halt) cs <= `IDLE;
                else if(cont) cs <= `EXECB;
                else cs <= `FETCHA;
        `EXECB:  if(cont) cs <= `EXECC;  
                 else cs <= `FETCHA;
        `EXECC:  cs <= `FETCHA;
        default: cs <= `IDLE;
      endcase

endmodule

module stack(clk, reset, load, push, pop, d, qtop, qnext);
  parameter N = 8;
	 
  input clk, reset, load, push, pop;
  input[15:0]d;
  output[15:0] qtop, qnext;
  reg [15:0] q [0:N-1];

  assign qtop = q[0];
  assign qnext = q[1];
   
  always @(posedge clk or negedge reset)
    if(!reset) q[0] <= 0;
    else if(load) q[0] <= d;
    else if(pop) q[0] <= q[1];

  integer i;
  always @(posedge clk or negedge reset)
    for(i=1;i< N-1;i=i+1)
      if(!reset) q[i] <= 0;
      else if(push) q[i] <= q[i-1];
      else if(pop) q[i] <= q[i+1];
   
  always @(posedge clk or negedge reset)
    if(!reset) q[N-1] <= 0;
    else if(push) q[N-1] <= q[N-2];
endmodule

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
// Write memory initialization here (e.g., mem[12'h001]=16'h1234;).
    mem[12'b000000000000] = 16'b0001100000000000 ;
    mem[12'b000000000001] = 16'b0011000000001110 ;
    mem[12'b000000000010] = 16'b0010000000001110 ;
    mem[12'b000000000011] = 16'b0001011111111111 ;
    mem[12'b000000000100] = 16'b1111000000001101 ;
    mem[12'b000000000101] = 16'b0101000000001101 ;
    mem[12'b000000000110] = 16'b0010000000001110 ;
    mem[12'b000000000111] = 16'b1110000000000000 ;
    mem[12'b000000001000] = 16'b0010000000001110 ;
    mem[12'b000000001001] = 16'b0001000000000001 ;
    mem[12'b000000001010] = 16'b1111000000000000 ;
    mem[12'b000000001011] = 16'b0011000000001110 ;
    mem[12'b000000001100] = 16'b0100000000000010 ;
    mem[12'b000000001101] = 16'b0000000000000000 ;
    mem[12'b000000001110] = 16'b0000000000000000 ;

 end
endmodule
module counter(clk,reset,load,inc,d,q);
  parameter N = 16;
   
  input clk,reset,load,inc;
  input[N-1:0] d;
  output[N-1:0] q;
  reg [ N-1:0 ] q ;

  always @(posedge clk or negedge reset)
    if(!reset) q <= 0;
    else if(load) q <= d;
    else if(inc) q <= q + 1;

endmodule


module alu(a, b, f, s);

 input[15:0] a, b;
 input[4:0]f;
 output[15:0]s;
 reg[15:0]s;
 wire[15:0] x, y;

 assign x = a + 16'h8000;
 assign y = b + 16'h8000;
  
 always @(a or b or x or y or f)
   case(f)
     `ADD : s = b + a;
     `SUB : s = b - a;
     `MUL : s = b * a;
     `SHL : s = b << a;
     `SHR : s = b >> a;
     `BAND: s = b & a;
     `BOR : s = b | a;
     `BXOR: s = b ^ a;
     `AND : s = b && a;
     `OR : s = b || a;
     `EQ : s = b == a;
     `NE : s = b != a;
     `GE : s = y >= x;
     `LE : s = y <= x;
     `GT : s = y > x;
     `LT : s = y < x;
     `NEG : s = -a;
     `BNOT : s = ~a;
     `NOT : s = !a;
     default : s = 16'hxxxx;
   endcase

endmodule

//---------------------------------------------------------------------------------------------------------------------------
// source: 
//      https://www.cs.hiroshima-u.ac.jp/~nakano/wiki/#p5
//---------------------------------------------------------------------------------------------------------------------------


module tinycpu(clk, reset, run, in, cs, pcout, irout, qtop, abus, dbus, out);

  input clk,reset,run;
  input[15:0] in;
  
  output[2:0]cs;
  output [15:0] irout, qtop, dbus, out;
  output[11:0] pcout, abus;

  reg [15:0] dbus_r;

  wire [15:0] qnext, ramout, aluout;
  reg[11:0] abus;
  reg halt, cont, pcinc, push, pop, abus2pc, dbus2ir, dbus2qtop, dbus2ram,
      dbus2obuf, pc2abus, ir2abus, ir2dbus, qtop2dbus, alu2dbus, ram2dbus,
      in2dbus, ind2abus;

  reg[11:0] ind_addr;
  reg ind_addr_ld;

  wire [11:0] ind_addr_next = irout[11:0] + qtop[11:0];

  counter #(12) pc0(.clk(clk), .reset(reset), .load(abus2pc), .inc(pcinc), .d(abus), .q(pcout));

  counter #(16) ir0(.clk(clk), .reset(reset), .load(dbus2ir), .inc(1'b0), .d(dbus), .q(irout));

  state state0(.clk(clk), .reset(reset), .run(run), .cont(cont), .halt(halt), .cs(cs));

  stack stack0(.clk(clk), .reset(reset), .load(dbus2qtop), .push(push), .pop(pop), .d(dbus), .qtop(qtop), .qnext(qnext));

  alu alu0(.a(qtop), .b(qnext), .f(irout[4:0]), .s(aluout));

  ram #(16,12,4096) ram0(.clk(clk), .load(dbus2ram), .addr(abus[11:0]), .d(dbus), .q(ramout));
  
  counter #(16) obuf0(.clk(clk), .reset(reset), .load(dbus2obuf), .inc(1'b0), .d(dbus), .q(out));

  // always @(pc2abus or ir2abus or ind2abus or pcout or irout or ind_addr)
  //   if(pc2abus) abus <= pcout;
  //   else if(ir2abus) abus <= irout[11:0];
  //   else if(ind2abus) abus <= ind_addr;
  //   else abus <= 12'hxxx;

  
  always @(*) begin
    if (pc2abus)      abus = pcout;
    else if (ir2abus) abus = irout[11:0];
    else if (ind2abus)abus = ind_addr;
    else              abus = pcout;  
  end

  // assign dbus = ir2dbus ? {{4{irout[11]}},irout[11:0]} : 16'hzzzz;
  // assign dbus = qtop2dbus ? qtop : 16'hzzzz;
  // assign dbus = alu2dbus ? aluout : 16'hzzzz;
  // assign dbus = ram2dbus ? ramout : 16'hzzzz;
  // assign dbus = in2dbus ? in : 16'hzzzz;

  assign dbus = dbus_r;
  always @(*) begin
    dbus_r = 16'h0000; 
    if (ir2dbus)       dbus_r = {{4{irout[11]}}, irout[11:0]};
    else if (qtop2dbus) dbus_r = qtop;
    else if (alu2dbus)  dbus_r = aluout;
    else if (ram2dbus)  dbus_r = ramout;
    else if (in2dbus)   dbus_r = in;
  end

  always @(cs or irout or qtop)
    begin
      halt = 0; pcinc = 0; push = 0; pop = 0; cont = 0; abus2pc = 0;
      dbus2ir = 0; dbus2qtop = 0; dbus2ram = 0; dbus2obuf = 0; pc2abus = 0;
      ir2abus = 0; ir2dbus = 0; qtop2dbus = 0; alu2dbus = 0; ram2dbus = 0;
      in2dbus = 0; ind2abus = 0; ind_addr_ld = 0;
      
      if(cs == `FETCHA)
        begin
          pcinc = 1; pc2abus = 1;
        end
      else if(cs == `FETCHB)
        begin
          ram2dbus = 1; dbus2ir = 1;
        end
      else if(cs == `EXECA)
        case(irout[15:12])
        `PUSHI:
           begin
             ir2dbus = 1; dbus2qtop = 1; push = 1;
           end	 
        `PUSH:
           begin
             ir2abus = 1; cont = 1;
           end
        `POP:
           begin
             ir2abus = 1; qtop2dbus = 1; dbus2ram = 1; pop = 1;
           end
        `JMP:
           begin
             ir2abus = 1; abus2pc = 1;
           end
        `JZ:
           begin
             if(qtop == 0)
               begin
                 ir2abus = 1; abus2pc = 1;
               end
             pop = 1;
           end
        `JNZ:
           begin
             if(qtop != 0)
               begin
                 ir2abus = 1; abus2pc = 1;
               end
             pop = 1;
           end
        `PUSH_IND:
           begin
              ind_addr_ld = 1; pop = 1; cont = 1;   
           end
        `POP_IND:
           begin
            ind_addr_ld = 1; pop = 1; cont = 1;
           end
        `IN:
           begin
             in2dbus = 1; dbus2qtop = 1; push = 1;
           end
        `OUT:
           begin
             qtop2dbus = 1; dbus2obuf = 1; pop = 1;
           end
        `OP:
           begin
             alu2dbus = 1; dbus2qtop = 1;
             if(irout[4] == 0) pop = 1;
           end
        default:
           halt = 1;
        endcase
      else if(cs == `EXECB)
        begin
          if(irout[15:12] == `PUSH)
            begin
              ram2dbus = 1; dbus2qtop = 1; push = 1;
            end
          else if(irout[15:12] == `PUSH_IND)
            begin
              ind2abus = 1; cont = 1;
            end
          else if(irout[15:12] == `POP_IND)
            begin
              ind2abus    = 1; qtop2dbus = 1; dbus2ram = 1; pop = 1;
            end
        end
      else if (cs == `EXECC) 
        begin
          if (irout[15:12] == `PUSH_IND) 
            begin
              ram2dbus   = 1; dbus2qtop = 1; push = 1;
            end
        end
    end    

    always @(posedge clk or negedge reset) 
      begin
        if(!reset) ind_addr <= 12'd0;
        else if(ind_addr_ld) ind_addr <= ind_addr_next;
        // else ind_addr <= 12'd0;
      end

    // always @ ( ind_addr_ld ) 
    //   begin
    //     if(ind_addr_ld) ind_addr = ind_addr_next;
    //   end

endmodule
