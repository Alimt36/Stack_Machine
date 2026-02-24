
`timescale 1ns / 1ps

`define IDLE   3'b000
`define FETCHA 3'b001
`define FETCHB 3'b010
`define EXECA  3'b011
`define EXECB  3'b100

module tinycpu_program_tb;

  reg         clk, reset, run;
  reg  [15:0] in;
  wire [2:0]  cs;
  wire [15:0] irout, qtop, dbus, out;
  wire [11:0] pcout, abus;

  tinycpu dut (
    .clk    (clk),
    .reset  (reset),
    .run    (run),
    .in     (in),
    .cs     (cs),
    .pcout  (pcout),
    .irout  (irout),
    .qtop   (qtop),
    .abus   (abus),
    .dbus   (dbus),
    .out    (out)
  );

  initial clk = 0;
  always #5 clk = ~clk;

  reg cpu_started;
  reg halt_reported;

  function signed [15:0] to_signed;
    input [15:0] val;
    begin
      to_signed = val;
    end
  endfunction

  initial begin
    in            = 16'h0000;
    reset         = 0;
    run           = 0;
    cpu_started   = 0;
    halt_reported = 0;

    $display("----------------------------------------------------------------------------------------------------");
    $display(" TinyCPU Program Execution");
    $display("----------------------------------------------------------------------------------------------------");

    #10;
    reset = 1;
    #10;
    
    run = 1;
    #10;
    
    $display("CPU started at t=%0t ns", $time);
    $display("----------------------------------------------------------------------------------------------------");
  end

  always @(posedge clk) begin
    if (!halt_reported && reset && run && cs != `IDLE)
      cpu_started <= 1;
  end

  always @(posedge clk) begin
    if (!halt_reported && cpu_started && cs == `IDLE) begin
      halt_reported <= 1;
      run <= 0;
      $display("----------------------------------------------------------------------------------------------------");
      $display("CPU HALTED at t=%0t ns", $time);
      $display("Final PC: %0d", pcout);
      if (out[15] == 1'b1)
        $display("Final OUT: 0x%04h (%0d)", out, to_signed(out));
      else
        $display("Final OUT: 0x%04h (%0d)", out, out);
      $display("----------------------------------------------------------------------------------------------------");
      $finish;
    end
  end

  always @(out) begin
    if (cpu_started && !halt_reported) begin
      if (out[15] == 1'b1)
        $display("[t=%0t] OUT = 0x%04h (%0d)", $time, out, to_signed(out));
      else
        $display("[t=%0t] OUT = 0x%04h (%0d)", $time, out, out);
    end
  end

  always @(posedge clk) begin
    if (cpu_started && !halt_reported) begin
      $display("t=%0t | CS=%b | PC=%0d | ir2dbus=%b qtop2dbus=%b alu2dbus=%b ram2dbus=%b in2dbus=%b | dbus=%h | out=%h",
               $time, cs, pcout,
               dut.ir2dbus, dut.qtop2dbus, dut.alu2dbus, dut.ram2dbus, dut.in2dbus,
               dbus, out);
    end
  end

  initial begin
    #1000000;
    $display("TIMEOUT - CPU did not halt");
    $finish;
  end

  initial begin
    $dumpfile("tinycpu_program_tb.vcd");
    $dumpvars(0, tinycpu_program_tb);
  end

endmodule

