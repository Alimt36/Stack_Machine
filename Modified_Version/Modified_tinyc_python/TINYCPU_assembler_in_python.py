
import os

OPCODES = {
    "HALT": "0000000000000000",

    "PUSHI"    : "0001",  # 0001iiiiiiiiiiii
    "PUSH"     : "0010",  # 0010aaaaaaaaaaaa
    "POP"      : "0011",  # 0011aaaaaaaaaaaa
        
    "PUSH_IND" : "0111",  # 0111( array base address )
    "POP_IND"  : "1000" , # 1000( array base address )

    "JMP"      : "0100",  # 0100aaaaaaaaaaaa
    "JZ"       : "0101",  # 0101aaaaaaaaaaaa
    "JNZ"      : "0110",  # 0110aaaaaaaaaaaa
    
    "IN"       : "1101000000000000",
    "OUT"      : "1110000000000000",
    
    "ADD"      : "1111000000000000",
    "SUB"      : "1111000000000001",
    "MUL"      : "1111000000000010",
    "SHL"      : "1111000000000011",
    "SHR"      : "1111000000000100",
    "BAND"     : "1111000000000101",
    "BOR"      : "1111000000000110",
    "BXOR"     : "1111000000000111",
    "AND"      : "1111000000001000",
    "OR"       : "1111000000001001",
    "EQ"       : "1111000000001010",
    "NE"       : "1111000000001011",
    "GE"       : "1111000000001100",
    "LE"       : "1111000000001101",
    "GT"       : "1111000000001110",
    "LT"       : "1111000000001111",
    "NEG"      : "1111000000010000",
    "BNOT"     : "1111000000010001",
    "NOT"      : "1111000000010010",
}

opcpde_16 = ["HALT","IN","OUT","ADD","SUB","MUL","SHL","SHR","BAND","BOR","BXOR" ,"AND","OR","EQ","NE","GE","LE","GT" , "LT" , "NEG" , "BNOT" , "NOT"]
opcode_j = ["JMP","JZ","JNZ"]
opcode_stack = ["PUSHI","PUSH","POP"]

labels = {}
line_counter = 0

mem_counter = 0
variables = {}

list_01s = []

#---------------------------------------------------------------------------------------------------------------------------
# file related functions : 
#   load_file : gets the absolute path of the c like code reads it to a string and outputs the text and the path 
#   save_0and1s_to_file : using the directory path of the c code saves the 0and1s output to the intended file 
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

def save_0and1s_to_file( path , x) : 
    file_source = path
    folder_path = os.path.dirname(file_source)
    temp = os.path.join(folder_path , "generated_0and1s.txt" )

    try : 
        with open(temp, "w") as f:
            f.writelines(x)
            print("-" * 100 )
            print(f"0and1s of the assembly generated! \nPath : {temp}")
            print("-" * 100 )
    except : 
            print("-" * 100 )
            print(f"Error while generating the 0amd1s_output_file , Please try again. ")
            print("-" * 100 )
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# generate_label :
#   generates the lablel that is needed for the various types of jumping in the stack assembly code 
#---------------------------------------------------------------------------------------------------------------------------
def label( line ) :
    global labels
    global line_counter

    temp = line.split(':')

    # print_and_add2list(temp)

    if temp[0] in labels :
        return 
    else : 
        labels.setdefault(temp[0] , line_counter)

#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# to_binary functions : 
#   they get a number and turn it into binary regarding the format they are written to
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
# calc_variable_address : 
#   the function is called when a "POP" is in the code and finds if the variable is difined or not and saves the memory-
#   -address of the variable to the dictionary (variables) for future usages 
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
# print_and_add2list : 
#   the function gets a str input appends the text to the list (list_01s) for the function (save_0and1s_to_file) to be-
#   -able to save the lines into the file and then prints the text to the terminal
#---------------------------------------------------------------------------------------------------------------------------
def print_and_add2list( text:str="\n" ) : 
    global list_01s
    
    print(text)
    list_01s.append(f"{text}\n")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
def main () :
    code_txt , path = load_file()

    global labels
    global line_counter
    global variables
    global mem_counter

    # for line in code_txt.split('\n'):
    #     line = line.strip() 
    #     if line:
    #         if line.startswith("POP") : 
    #             calc_variable_address(line)
    # line_counter = mem_counter 

    # print_and_add2list(variables)


    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            if ":" in line : 
                # print_and_add2list("!")
                label( line )
            else : 
                line_counter += 1


    mem_counter = line_counter
    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            if line.startswith("POP") and not(line.startswith("POP_IND")) : 
                calc_variable_address(line)


    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            parts = line.split(' ')
            if parts[0] in opcpde_16 : 
                # pass
                print_and_add2list(f"{OPCODES[parts[0]]}")
            elif parts[0] in opcode_stack : 
                if parts[0] == "PUSHI" : 
                    print_and_add2list(f"{OPCODES[parts[0]]}{int_2_binary_12bit(int(parts[1]))}")
                else : 
                    print_and_add2list(f"{OPCODES[parts[0]]}{int_2_binary_12bit(variables[parts[1]])}")
            elif parts[0] in opcode_j : 
                print_and_add2list(f"{OPCODES[parts[0]]}{int_2_binary_12bit(labels[parts[1]])}")
            elif parts[0] == "POP_IND" : 
                print_and_add2list(f"1000{ int_2_binary_12bit( variables[f"{parts[1]}0"] ) }")
            elif parts[0] == "PUSH_IND" : 
                # pass
                print_and_add2list(f"0111{ int_2_binary_12bit( variables[f"{parts[1]}0"] ) }")


    for _0   in variables : 
        # print_and_add2list(int_2_binary_16bit( variables[_0] ))
        print_and_add2list(int_2_binary_16bit( 0 ))

    # print_and_add2list( "\n" , labels)
    save_0and1s_to_file( path , list_01s )

main()
#---------------------------------------------------------------------------------------------------------------------------
