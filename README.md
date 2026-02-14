## Repository Structure
The repository is divided into 2 main parts, Hardware and Software. The following tree shows the file structure of the repository and then the parts will be explained separately.
```
tinycpu/
├── hardware/
│   ├── tinycpu.v
│   ├── tinycpu_tb.v
│   └── modules/
│       ├── alu.v
│       ├── stack.v
│       ├── ram.v
│       ├── counter.v
│       └── state.v
│
├── compiler-assembler/
│   │
│   ├── legacy/            # Original Perl/Lex/Yacc toolchain
│   │   ├── tinyc.l
│   │   ├── tinyc.y
│   │   └── asm.pl
│   │
│   └── python/            # Python-based toolchain
│       ├── TINYCPU_compiler_in_python.py
│       ├── TINYCPU_assembler_in_python.py
│       ├── TINYCPU_mac2mem_in_python.py
│       └── TINYCPU_toolchain_controler.py
│
├── docs/
│   ├── ...
│   └── ...
│
└── README.md
```
---
## Hardware Part:
### TINYCPU: A Stack Machine - A 16-bit Stack-Based Processor

The architecture and design of the CPU is from the University of Hiroshima and engineers there.  
Source code address: [source](https://www.cs.hiroshima-u.ac.jp/~nakano/wiki/#p5)

The CPU is FPGA-friendly and can be implemented efficiently on FPGA boards.

### Architecture:
In one word: Every operation is a stack operation!

![TinyCPU Architecture](pdf_s/TINYCPU_Architecture.png)

- **Data Width:** 16-bit
- **Architecture:** Stack-based (8-level stack)
- **Memory:** 256 words RAM (configurable up to 4096)
- **ALU Operations:** 19 operations including arithmetic, logical, bitwise, and comparison
- **Instruction Set:** 12 instruction types
- **State Machine:** 5-state fetch-decode-execute cycle

**Instruction Set:**
```python
"HALT": "0000000000000000",

"PUSHI": "0001",  # 0001iiiiiiiiiiii
"PUSH" : "0010",  # 0010aaaaaaaaaaaa
"POP"  : "0011",  # 0011aaaaaaaaaaaa

"JMP"  : "0100",  # 0100aaaaaaaaaaaa
"JZ"   : "0101",  # 0101aaaaaaaaaaaa
"JNZ"  : "0110",  # 0110aaaaaaaaaaaa

"IN"   : "1101000000000000",
"OUT"  : "1110000000000000",

"ADD"  : "1111000000000000",
"SUB"  : "1111000000000001",
"MUL"  : "1111000000000010",
"SHL"  : "1111000000000011",
"SHR"  : "1111000000000100",
"BAND" : "1111000000000101",
"BOR"  : "1111000000000110",
"BXOR" : "1111000000000111",
"AND"  : "1111000000001000",
"OR"   : "1111000000001001",
"EQ"   : "1111000000001010",
"NE"   : "1111000000001011",
"GE"   : "1111000000001100",
"LE"   : "1111000000001101",
"GT"   : "1111000000001110",
"LT"   : "1111000000001111",
"NEG"  : "1111000000010000",
"BNOT" : "1111000000010001",
"NOT"  : "1111000000010010",
```
---

## Software Part:
### Compiler-Assembler:

The source code provides a toolchain that can compile and assemble from a C-like language to the Verilog memory format, but I found it a bit hard to use and confusing, so I wrote a toolchain myself in Python that is really user-friendly!

**The Python compiler-assembler I wrote:**
- **TINYCPU_compiler_in_python.py:** Gets the C-like code address and generates the stack assembly
- **TINYCPU_assembler_in_python.py:** Gets the stack assembly and generates the binary
- **TINYCPU_mac2mem_in_python.py:** Gets the binary code and converts it to Verilog memory initialization format
- **TINYCPU_toolchain_controler.py:** Connects all 3 codes above for ease of use; only needs the path of the C-like code and does everything needed

![compiler-assembler in python](tinyc_python/py_code_pic_for_readme.png)

**The C-like language:**

The C-like language that the compiler accepts has the following rules:
- Variable definition: only one per line
- Array support : supports only consistant indexing because of hardware limitations! and doesn't handle initialization by value  
- Math operations: only one per line and must be in the format `{operand0 operation operand1}`
- If-else and while: supported but must be written in one line
- Characters of different purposes are better separated by spaces

**A valid example:**
```c
int x = 36 ;
int y ;
int i ;
int Some_Array[10] ;

while ( i <= 10 ) { if ( x == 36 ) { out( 1 ) ; i = i + 1 ; } else { out( 0 ) ; } }

if ( x == 36 ) { out( 1 ) ; i = i + 1 ; } else { out( 0 ) ; }

Some_Array[9] = Some_Array[0] + x ;

halt;
```
---
## Usage Flow:
1. Write the code in C-like language
2. Use the Python toolchain to get memory initialization lines for the CPU
3. Add the memory initialization lines to the `ram.v` module
4. Implement the CPU on a FPGA
5. Let the CPU run your code!
---
                                                                                                                 
by Alimt36 