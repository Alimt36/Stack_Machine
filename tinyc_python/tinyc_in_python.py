
import re as regex

#---------------------------------------------------------------------------------------------------------------------------
# Code file Load
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

    return code_txt
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
operation_str = ""
line_end:bool = 0

Invalid_Syntax:bool = 0
#---------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------
# math operations
#---------------------------------------------------------------------------------------------------------------------------
def math_operation ( code_txt ) :
    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:  
            parts = regex.split(r'([+\-*;])', line)
            for chars in parts : 
                chars.strip()
                if chars :
                    try :
                        x = int(chars)
                        # print(x)
                        print(f"PUSHI {x}")
                    except :
                        if chars != ' ' :
                            if   chars == '+' : operation_str = "ADD"
                            elif chars == '-' : operation_str = "SUB"
                            elif chars == '*' : operation_str = "MUL"
                            elif chars == ';' : line_end = 1
                            else :
                                print("Invalid Syntax") 
                                operation_str = "-1"
            print(operation_str)
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# variable defenition
#---------------------------------------------------------------------------------------------------------------------------
def save_variable ( i , parts , value ) :
    global Invalid_Syntax
    if value == None :
        try :
            x = int(parts[i+2])
            print(f"PUSHI {x}")
            print(f"POP {parts[i]}")
        except :
            print("Invalid Syntax") 
            Invalid_Syntax = 1
            return
    else :
        x = value
        print(f"PUSHI {x}")
        print(f"POP {parts[i]}")

def variable_definition( code_txt  ) :
    global Invalid_Syntax
    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:
            parts = line.split(' ')
            if parts[0] == "int" : 
                for i in range (1 , len(parts)) :
                    try : 
                        if parts[(i + 1)] == "=" :
                            save_variable(i , parts , None)
                            break
                        elif  parts[(i + 1)] == ";" : 
                            save_variable(i , parts , 0)
                            break
                        else : 
                            print("Invalid Syntax") 
                            Invalid_Syntax = 1
                    except : 
                        print("Invalid Syntax") 
#---------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------
# main
#---------------------------------------------------------------------------------------------------------------------------

def main () : 

    code_txt = load_file()

    for line in code_txt.split('\n'):
        line = line.strip() 

    variable_definition( code_txt )
    math_operation( code_txt )


main()
#---------------------------------------------------------------------------------------------------------------------------
