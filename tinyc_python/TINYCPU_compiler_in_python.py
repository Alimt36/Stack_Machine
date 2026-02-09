
import os
import re as regex

#---------------------------------------------------------------------------------------------------------------------------
operation_str = ""
line_end:bool = 0

Invalid_Syntax:bool = 0

label_counter = 0

asm_list = []
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# file related functions : 
#   load_file : gets the absolute path of the c like code reads it to a string and outputs the text and the path 
#   save_assembly_to_file : using the directory path of the c code saves the stack assembly output to the intended file 
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

def save_assembly_to_file( path , assembly_list) : 
    file_source = path
    folder_path = os.path.dirname(file_source)
    assebly_output_file_path = os.path.join(folder_path , "generated_assebly.txt" )

    try : 
        with open(assebly_output_file_path, "w") as f:
            f.writelines(assembly_list)
            print("-" * 100 )
            print(f"Assembly of the code generated! \nPath : {assebly_output_file_path}")
            print("-" * 100 )
    except : 
            print("-" * 100 )
            print(f"Error while generating the assebly_output_file , Please try again. ")
            print("-" * 100 )
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# math operations : 
#   the function can handle the operations that have only 2 operands and one operation and the operands must be separated-
#   -from the operation 
#       --> template : { operand0 operation operand1 }
#---------------------------------------------------------------------------------------------------------------------------
def math_operation ( line ) :
    parts = regex.split(r'([+\-*;])', line)
    for chars in parts : 
        chars.strip()
        if chars :
            try :
                x = int(chars)
                # print(x)
                print_and_add2list(f"PUSHI {x}")
            except :
                if chars != ' ' :
                    if   chars == '+' : operation_str = "ADD"
                    elif chars == '-' : operation_str = "SUB"
                    elif chars == '*' : operation_str = "MUL"
                    elif chars == ';' : line_end = 1
                    else :
                        # print("Invalid Syntax") 
                        # operation_str = "-1"
                        print_and_add2list(f"PUSH {chars.strip()}")
    print_and_add2list(operation_str)
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# variable related functions : 
#   save_variable : a function that saves the value with two modes: one is with value and one is without a value which in  -
#       - that case saves 0 by default
#   variable_definition : when a "int" is there it is called and saves the variable
#   save_value : saves a value to a defined variable
#   save_value_by_variable : a better function that saves a value to a variable  
#---------------------------------------------------------------------------------------------------------------------------
def save_variable ( i , parts , value ) :
    global Invalid_Syntax
    if value == None :
        try :
            x = int(parts[i+2])
            print_and_add2list(f"PUSHI {x}")
            print_and_add2list(f"POP {parts[i]}")
        except :
            print("Invalid Syntax") 
            Invalid_Syntax = 1
            return
    else :
        x = value
        print_and_add2list(f"PUSHI {x}")
        print_and_add2list(f"POP {parts[i]}")

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

def save_value( var , val=0 ) :

    if val != None :
        try :
            x = int(val)
            print_and_add2list(f"PUSHI {x}")
            print_and_add2list(f"POP {var}")
            return True
        except : 
            # Invalid_Syntax = 1
            return False
    else : 
        print_and_add2list(f"POP {var}")   

def save_value_by_variable(var , val ) : 
    
    try : 
        x = int(val)
        print_and_add2list(f"PUSHI {x}")
        print_and_add2list(f"POP {var}")
        return True
    except :
        print_and_add2list(f"PUSH {val}") 
        print_and_add2list(f"POP {var}")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# out handler :
#   the out must be a single varible or a single number ! 
#---------------------------------------------------------------------------------------------------------------------------
def out_handler( line ) : 
    temp1 = 0
    temp2 = 0
    for _ in range ( 0 , len(line)) : 
        if line[_] == '(' : temp1 = _
        elif line[_] == ')' : temp2 = _
        
    temp = line[temp1+1:temp2]
    temp = temp.strip()
    try:
        x = int(temp)
        print_and_add2list(f"PUSHI {x}")
        print_and_add2list("OUT")
    except:
        print_and_add2list(f"PUSH {temp}")
        print_and_add2list("OUT")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# if handler :
#   split_statements_safely : splits the statements while being aware of the braces and parentheses , used when there are-
#       -multiple statements in the body of the if or while and we need to separate them without breaking nested structures
#   handle_one_line_if : handles if statements without else block , generates labels for jumping and processes the body-
#       -statements whether they are in braces or single statement
#   handle_one_line_if_else : handles if-else statements , generates two labels (F for false/else block and T for true/-
#       -end) and processes both if and else bodies separately
#   parse_condition : extracts the left operand , operator and right operand from the condition , generates the appropriate-
#       -comparison code (PUSH/PUSHI for operands and comparison instruction like GT,EQ,etc)
#   parse_statement : the main statement parser that determines the type of statement (out, halt, if, assignment) and calls-
#       -the appropriate handler , used recursively for nested if statements inside while loops
#   if_handler : the main if dispatcher that checks if the line contains else keyword and calls the appropriate handler-
#       -(handle_one_line_if or handle_one_line_if_else)
#---------------------------------------------------------------------------------------------------------------------------
def split_statements_safely(s: str):
    stmts = []
    cur = []
    brace = 0
    paren = 0

    for ch in s:
        if ch == '{':
            brace += 1
        elif ch == '}':
            brace -= 1
        elif ch == '(':
            paren += 1
        elif ch == ')':
            paren -= 1

        if ch == ';' and brace == 0 and paren == 0:
            stmt = ''.join(cur).strip()
            if stmt:
                stmts.append(stmt)
            cur = []
        else:
            cur.append(ch)

    tail = ''.join(cur).strip()
    if tail:
        stmts.append(tail)

    return stmts

def handle_one_line_if(condition, body):
    label_num = generate_label()
    parse_condition(condition)
    print_and_add2list(f"JZ _{label_num:03d}F")
    
    body = body.strip()
    if body.startswith('{') and body.endswith('}'):
        body = body[1:-1].strip()
        statements = body.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                parse_statement(stmt)
    else:
        parse_statement(body)
    
    print_and_add2list(f"_{label_num:03d}F:")


def handle_one_line_if_else(condition, if_body, else_body):
    label_num = generate_label()

    parse_condition(condition)
    print_and_add2list(f"JZ _{label_num:03d}F")

    if_body = if_body.strip()
    if if_body.startswith('{') and if_body.endswith('}'):
        if_body = if_body[1:-1].strip()
        statements = if_body.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                parse_statement(stmt)
    else:
        parse_statement(if_body)

    print_and_add2list(f"JMP _{label_num:03d}T")
    print_and_add2list(f"_{label_num:03d}F:")

    else_body = else_body.strip()
    if else_body.startswith('{') and else_body.endswith('}'):
        else_body = else_body[1:-1].strip()
        statements = else_body.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                parse_statement(stmt)
    else:
        parse_statement(else_body)

    print_and_add2list(f"_{label_num:03d}T:")

def parse_condition(condition):
    ops = {
        '>=': 'GE', '<=': 'LE', '==': 'EQ', '!=': 'NE',
        '>': 'GT', '<': 'LT'
    }
    
    for op_str, op_code in ops.items():
        if op_str in condition:
            parts = condition.split(op_str)
            left = parts[0].strip()
            right = parts[1].strip()
            
            try:
                x = int(left)
                print_and_add2list(f"PUSHI {x}")
            except:
                print_and_add2list(f"PUSH {left}")
            
            try:
                x = int(right)
                print_and_add2list(f"PUSHI {x}")
            except:
                print_and_add2list(f"PUSH {right}")
            
            print_and_add2list(op_code)
            return
    
    print("Error: No comparison operator found in condition")

def parse_statement(stmt):
    stmt = stmt.strip()
    
    if stmt.startswith("out("):
        out_handler(stmt)
    
    elif stmt.startswith("halt"):
        halt_handler(stmt)
    
    elif stmt.startswith("if"):
        if_handler(stmt)
    
    elif '=' in stmt:
        stmt = stmt.rstrip(';').strip()
        parts = stmt.split()
        
        if len(parts) == 3:
            save_value_by_variable(parts[0], parts[2])
        elif len(parts) == 5:
            math_operation(f"{parts[2]} {parts[3]} {parts[4]}")
            save_value(parts[0], None)
        else:
            print(f"// Error: unexpected assignment format ({len(parts)} parts): {stmt}")
            print(f"// Parts: {parts}")
    
    else:
        print(f"// Unknown statement: {stmt}")
 
def if_handler( line ) :
    # if '{' not in line:
        if 'else' in line:
            match = regex.match(r'if\s*\((.*?)\)\s*(.*?)\s*else\s*(.*)', line)
            if match:
                condition = match.group(1)
                if_body = match.group(2)
                else_body = match.group(3)
                handle_one_line_if_else(condition, if_body, else_body)
        else:
            match = regex.match(r'if\s*\((.*?)\)\s*(.*)', line)
            if match:
                condition = match.group(1)
                body = match.group(2)
                handle_one_line_if(condition, body)
    # else:
    #     print("// Multi-line if not supported yet")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# generate_label :
#   generates the lablel that is needed for the various types of jumping in the stack assembly code 
#---------------------------------------------------------------------------------------------------------------------------
def generate_label():
    global label_counter
    label_counter += 1
    return label_counter
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# halt handler
#---------------------------------------------------------------------------------------------------------------------------
def halt_handler( line ) :
    print_and_add2list(f"HALT")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# while : 
#   One-line while handler that supports multiple statements in { }
#---------------------------------------------------------------------------------------------------------------------------
def while_handler(condition, body):
    label_num = generate_label()
    
    print_and_add2list(f"_{label_num:03d}T:")
    
    parse_condition(condition)
    
    print_and_add2list(f"JZ _{label_num:03d}F")
    
    body = body.strip()
    
    if body.startswith('{') and body.endswith('}'):
        body = body[1:-1].strip()

        # statements = body.split(';')
        statements = split_statements_safely(body)
        
        for stmt in statements:
            stmt = stmt.strip()
            if stmt: 
                parse_statement(stmt)
    else:
        parse_statement(body)
    
    print_and_add2list(f"JMP _{label_num:03d}T")
    print_and_add2list(f"_{label_num:03d}F:")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
# print_and_add2list : 
#   the function gets a str input appends the text to the list (asm_list) for the function (save_assembly_to_file) to be-
#   -able to save the lines into the file and then prints the text to the terminal
#---------------------------------------------------------------------------------------------------------------------------
def print_and_add2list( text:str="\n" ) : 
    global asm_list
    
    print(text)
    asm_list.append(f"{text}\n")
#---------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------
def main () : 

    code_txt , path = load_file()

    for line in code_txt.split('\n'):
        line = line.strip() 
        if line:  
            if line[0:2] != "//" :
                parts = line.split(' ')

                if parts[0] == "int" :
                    variable_definition( parts )

                elif len(parts) > 1 and parts[1] == "=" :
                    if len(parts) == 4 :
                        save_value_by_variable( parts[0] , parts[2] )
                    else :
                        math_operation( f"{parts[2]} {parts[3]} {parts[4]}" )
                        save_value(parts[0] , None)
                
                elif line.startswith("out(") :
                    out_handler(line)

                elif (line.startswith("halt;")) or ( len(line) > 1 and line.startswith("halt") and parts[1] == ";" ) :
                    halt_handler(line)

                elif line.startswith("if") : 
                    # print("!!!")
                    if_handler( line )
                elif line.startswith("while"):
                    match = regex.match(r'while\s*\((.*?)\)\s*(.*)', line)
                    if match:
                        condition = match.group(1)
                        body = match.group(2)
                        while_handler(condition, body)

    global asm_list
    save_assembly_to_file( path , asm_list )

main()
#---------------------------------------------------------------------------------------------------------------------------
