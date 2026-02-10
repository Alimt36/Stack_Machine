# TINYCPU : A Stack_Machine : A 16-bit Stack-Based Processor

the architecture and the design of the cpu is for the university of the hiroshima and engineers there 
the source code address : [source](https://www.cs.hiroshima-u.ac.jp/~nakano/wiki/#p5)

the cpu is fpga-friendly and can get implemented really good on the fpga boards.

# Architecture
![TinyCPU Architecture](pdf_s/TINYCPU_Architecture.png)

-Data Width: 16-bit                                      
-Architecture: Stack-based (8-level stack)                                              
-Memory: 256 words RAM (configurable up to 4096)                                           
-ALU Operations: 19 operations including arithmetic, logical, bitwise, and comparison                            
-Instruction Set: 12 instruction types                                                         
-State Machine: 5-state fetch-decode-execute cycle                                      

Instruction Set:
| Opcode | Instruction |
|--------|-------------|
| 0000 | HALT |
| 0001 | PUSHI
| 0010 | PUSH |
| 0011 | POP | 
| 0100 | JMP | 
| 0101 | JZ |
| 0110 | JNZ |
| 1101 | IN |
| 1110 | OUT |
| 1111 | OP |

---
# Repository Structure
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
├── docs/
│   ├── ...
│   └── ...
│
├── toolchain/
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
└── README.md
```
---