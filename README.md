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

## Software part:
### compiler-assembler:
the source code provides a toolchain that can compile and assemble from a c like language to the verilog memory format, but i find it a bit hard to use and confusing, so I wrote a toolchain myself that is python and is really user-friendly!

**the python compiler-assembler that i wrote:**
- TINYCPU_compiler_in_python.py : gets the c like code address and generate the stack-assembly 
- TINYCPU_assembler_in_python.py : gets the stack-assembly and generates the binary of it
- TINYCPU_mac2mem_in_python.py : gets the binary of the code and turns it into the format of the verilog memory initialization format 
- TINYCPU_toolchain_controler.py : connect all the 3 codes above for ease of use,it only need path of the c like code and does everything needed

![compiler-assembler in python](tinyc_python/py_code_pic_for_readme.png)
