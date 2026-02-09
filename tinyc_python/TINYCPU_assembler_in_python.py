
OPCODES = {
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
}

opcpde_16 = ["HALT","IN","OUT","ADD","SUB","MUL","SHL","SHR","BAND","BOR","BXOR" ,"AND","OR","EQ","NE","GE","LE","GT" , "LT" , "NEG" , "BNOT" , "NOT"]
opcode_j = ["JMP","JZ","JNZ"]
opcode_stack = ["PUSHI","PUSH","POP"]

# labels : []
labels = {}
line_counter = 0

mem_counter = 0
variables = {}
#---------------------------------------------------------------------------------------------------------------------------
# load assembly file
#---------------------------------------------------------------------------------------------------------------------------
def load_file () -> str : 
    path = input("Path of the code : ")

    with open(path, "r", encoding="utf-8") as f:
        code_txt = f.read()

    print("-" * 100 )
    print(path)
    print("-" * 100 )
    print(code_txt)
    print("-" * 100 )

    return code_txt , path
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# lablel handler
#---------------------------------------------------------------------------------------------------------------------------
def label( line ) :
    global labels
    global line_counter

    temp = line.split(':')

    # print(temp)

    if temp[0] in labels :
        return 
    else : 
        labels.setdefault(temp[0] , line_counter)

#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# 
#---------------------------------------------------------------------------------------------------------------------------
def int_2_binary_12bit ( labelnum ) : 
    temp = bin(labelnum)[2:]
    temp_0s = '0' * (12-len(temp)) 
    temp_str = f"{temp_0s}{temp}"

    return temp_str

def int_2_binary_16bit ( x ) : 
    temp = bin(x)[2:]
    temp_0s = '0' * (16-len(temp)) 
    temp_str = f"{temp_0s}{temp}"

    return temp_str
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
#
#---------------------------------------------------------------------------------------------------------------------------
def calc_variable_address ( line ) : 
    global variables
    global mem_counter

    temp = line.split(' ')

    if temp[1] in variables:
        return
    else : 
        variables.setdefault(temp[1] , mem_counter)
        mem_counter += 1

#---------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------
# main
#---------------------------------------------------------------------------------------------------------------------------

def main () :
    code_txt , path = load_file()

    global labels
    global line_counter
    global variables
    global mem_counter

    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            if line.startswith("POP") : 
                calc_variable_address(line)

    # print(variables)

    line_counter = mem_counter + 1

    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            if ":" in line : 
                # print("!")
                label( line )
            else : 
                line_counter += 1

    for _0   in variables : 
        # print(int_2_binary_16bit( variables[_0] ))
        print(int_2_binary_16bit( 0 ))

    # print("!")
    # print("!")
    # print("!")

    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            parts = line.split(' ')
            if parts[0] in opcpde_16 : 
                # pass
                print(f"{OPCODES[parts[0]]}")
            elif parts[0] in opcode_stack : 
                if parts[0] == "PUSHI" : 
                    print(f"{OPCODES[parts[0]]}{int_2_binary_12bit(int(parts[1]))}")
                else : 
                    print(f"{OPCODES[parts[0]]}{int_2_binary_12bit(variables[parts[1]])}")
            elif parts[0] in opcode_j : 
                print(f"{OPCODES[parts[0]]}{int_2_binary_12bit(labels[parts[1]])}")


    # print( "\n" , labels)

main()
#---------------------------------------------------------------------------------------------------------------------------
