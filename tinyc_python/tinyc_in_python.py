
import re as regex

#---------------------------------------------------------------------------------------------------------------------------
operation_str = ""
line_end:bool = 0

Invalid_Syntax:bool = 0
#---------------------------------------------------------------------------------------------------------------------------

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
# math operations
#---------------------------------------------------------------------------------------------------------------------------
def math_operation ( line ) :
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
                        # print("Invalid Syntax") 
                        # operation_str = "-1"
                        print(f"PUSH {chars.strip()}")
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

def variable_definition( parts  ) :
    global Invalid_Syntax 
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
# save a value into a varible 
#---------------------------------------------------------------------------------------------------------------------------
def save_value( var , val=0 ) :

    if val != None :
        try :
            x = int(val)
            print(f"PUSHI {x}")
            print(f"POP {var}")
            return True
        except : 
            # Invalid_Syntax = 1
            return False
    else : 
        print(f"POP {var}")    
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# out() handling
#   the out must be a single varible or a single number ! 
#---------------------------------------------------------------------------------------------------------------------------
def out_handler( line ) : 
    temp1 = 0
    temp2 = 0
    for _ in range ( 0 , len(line)) : 
        if line[_] == '(' : temp1 = _
        elif line[_] == ')' : temp2 = _

    try:
        x = int(line[temp1+1:temp2])
        print(f"PUSHI {line[temp1+1:temp2]}")
        print("OUT")
    except:
        print(f"PUSH {line[temp1+1:temp2]}")
        print("OUT")

    # print(f"temp1 : {temp1}")
    # print(f"temp2 : {temp2}")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# halt handling
#---------------------------------------------------------------------------------------------------------------------------
def halt_handler( line ) :
    print(f"HALT")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# main
#---------------------------------------------------------------------------------------------------------------------------

def main () : 

    code_txt = load_file()

    # for line in code_txt.split('\n'):
    #     line = line.strip() 

    # variable_definition( code_txt )
    # math_operation( code_txt )





    # save_value( "x" , None)


    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:  
            parts = line.split(' ')
            if parts[0] == "int" :
                variable_definition( parts )
            elif len(parts) > 1 and parts[1] == "=" :
                math_operation( f"{parts[2]} {parts[3]} {parts[4]}" );
                save_value(parts[0] , None);
            elif line.startswith("out(") :
                out_handler(line)
            elif line.startswith("halt;") :
                halt_handler(line) 



main()
#---------------------------------------------------------------------------------------------------------------------------
