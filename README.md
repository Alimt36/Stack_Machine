## Repository Structure
```
tinycpu/
├── hardware/
│   ├── tinycpu.v
│   ├── tinycpu_tb.v
│   └── modules
│       ├── alu.v
│       ├── stack.v
│       ├── ram.v
│       ├── counter.v
│       └── state.v
│
├── compiler-assembler/
|   |
│   ├── legacy/            # Original Perl/Lex/Yacc toolchain
|   |   |
│   │   ├── tinyc.l
│   │   ├── tinyc.y
│   │   └── asm.pl
│   │
│   └── python/            # Python-based toolchain
|       |
│       ├── TINYCPU_compiler_in_python.py
│       ├── TINYCPU_assembler_in_python.py
│       ├── TINYCPU_mac2mem_in_python.py
│       └── TINYCPU_build_all.py
│
├── docs/
│   ├── ...
│   └── ...
|
└── README.md
```
---
## Hardware part: 
### TINYCPU: A Stack Machine: A 16-bit Stack-Based Processor

the architecture and the design of the cpu is for the university of the hiroshima and engineers there                
the source code address : [source](https://www.cs.hiroshima-u.ac.jp/~nakano/wiki/#p5)

the cpu is fpga-friendly and can get implemented really good on the fpga boards.

### Architecture
- In one word : Every operation is a stack operation!
![TinyCPU Architecture](pdf_s/TINYCPU_Architecture.png)

- Data Width: 16-bit                                      
- Architecture: Stack-based (8-level stack)                                              
- Memory: 256 words RAM (configurable up to 4096)                                           
- ALU Operations: 19 operations including arithmetic, logical, bitwise, and comparison                            
- Instruction Set: 12 instruction types                                                         
- State Machine: 5-state fetch-decode-execute cycle                                      

Instruction Set:
```
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

## Software part:
### compiler-assembler:
the source code provides a toolchain that can compile and assemble from a c like language to the verilog memory format, but i find it a bit hard to use and confusing, so I wrote a toolchain myself that is in python and is really user-friendly!

**the python compiler-assembler that i wrote:**
- TINYCPU_compiler_in_python.py : gets the c like code address and generate the stack-assembly 
- TINYCPU_assembler_in_python.py : gets the stack-assembly and generates the binary of it
- TINYCPU_mac2mem_in_python.py : gets the binary of the code and turns it into the format of the verilog memory initialization format 
- TINYCPU_toolchain_controler.py : connect all the 3 codes above for ease of use,it only need path of the c like code and does everything needed

![compiler-assembler in python](tinyc_python/py_code_pic_for_readme.png)

**the c-like language:**
the c-like language that the compiler accepts is as follows : 
- variable defenition only one per line!
- math operation only one per line and must be in the format of {operand0 operation operand1} !
- if-else and while supported but must be written in one line!
- the characters of diffrent purpose is better to be seprated by space! 

a valid example: 
```
int x = 36 ;
int y ;
int i ;

while ( i <= 10 ) { if ( x == 36 ) { out( 1 ) ; i = i + 1 ; } else { out( 0 ) ; } }

if ( x == 36 ) { out( 1 ) ; i = i + 1 ; } else { out( 0 ) ; }

halt;
```