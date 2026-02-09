
import os

mac2mem_list = []

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

def print_and_add2list( text:str="\n" ) : 
    global mac2mem_list
    
    print(text)
    mac2mem_list.append(f"{text}\n")

def int_2_binary_16bit ( x ) : 
    temp = bin(x)[2:]
    temp_0s = '0' * (16-len(temp)) 
    temp_str = f"{temp_0s}{temp}"

    return temp_str

def main() : 
     
    code_txt , path = load_file()

    mem_counter = 0

    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            print_and_add2list(f"mem[16'b{int_2_binary_16bit(mem_counter)}] = 12'b{line} ;")
            mem_counter += 1
main()