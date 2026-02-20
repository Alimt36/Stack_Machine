
import os

mac2mem_list = []

#---------------------------------------------------------------------------------------------------------------------------
# file related functions : 
#   load_file : gets the absolute path of the c like code reads it to a string and outputs the text and the path 
#   save_mac2mem_to_file : using the directory path of the c code saves the 0and1s in the verilog format output to the-
#    -intended file  
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

def save_mac2mem_to_file( path , x) : 
    file_source = path
    folder_path = os.path.dirname(file_source)
    temp = os.path.join(folder_path , "generated_mac2mem.txt" )

    try : 
        with open(temp, "w") as f:
            f.writelines(x)
            print("-" * 100 )
            print(f"mac2mem of the 0and1s generated! \nPath : {temp}")
            print("-" * 100 )
    except : 
            print("-" * 100 )
            print(f"Error while generating the 0amd1s_output_file , Please try again. ")
            print("-" * 100 )
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# print_and_add2list : 
#   the function gets a str input appends the text to the list (mac2mem_list) for the function (save_mac2mem_to_file) to be-
#   -able to save the lines into the file and then prints the text to the terminal
#---------------------------------------------------------------------------------------------------------------------------
def print_and_add2list( text:str="\n" ) : 
    global mac2mem_list
    
    print(text)
    mac2mem_list.append(f"{text}\n")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# to_binary functions : 
#   they get a number and turn it into binary regarding the format they are written to
#---------------------------------------------------------------------------------------------------------------------------
def int_2_binary_16bit ( x ) : 
    temp = bin(x)[2:]
    temp_0s = '0' * (16-len(temp)) 
    temp_str = f"{temp_0s}{temp}"

    return temp_str

def int_2_binary_12bit ( labelnum ) : 
    temp = bin(labelnum)[2:]
    temp_0s = '0' * (12-len(temp)) 
    temp_str = f"{temp_0s}{temp}"

    return temp_str
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
def main() : 
     
    code_txt , path = load_file()

    mem_counter = 0

    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            print_and_add2list(f"mem[12'b{int_2_binary_12bit(mem_counter)}] = 16'b{line} ;")
            mem_counter += 1

    save_mac2mem_to_file( path , mac2mem_list )
main()
#---------------------------------------------------------------------------------------------------------------------------
