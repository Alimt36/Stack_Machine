
import os
import subprocess
import sys
import time

#---------------------------------------------------------------------------------------------------------------------------
# run_script_with_input : 
#   runs a python script as a subprocess and automatically provides the input path when the script prompts for it , returns-
#   -True if successful and False if there was an error
#---------------------------------------------------------------------------------------------------------------------------
def run_script_with_input(script_name, input_path):
    print("-" * 100)
    print(f"Running: {script_name}")
    print("-" * 100)
    
    try:
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=input_path + "\n")
        
        print(stdout)
        
        if stderr:
            print("STDERR:", stderr)
        
        if process.returncode != 0:
            print(f"ERROR: {script_name} failed with return code {process.returncode}")
            time.sleep(2)
            return False
        
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"ERROR running {script_name}: {e}")
        time.sleep(2)
        return False
#---------------------------------------------------------------------------------------------------------------------------    

#---------------------------------------------------------------------------------------------------------------------------
# main : 
#   the build pipeline that takes a c code file path , locates the compiler/assembler/mac2mem scripts in the same folder-
#   -and runs them in sequence to generate assembly, binary and verilog memory initialization files
#---------------------------------------------------------------------------------------------------------------------------
def main():
    c_code_path = input("Enter path to C code file: ").strip()
    
    if not os.path.exists(c_code_path):
        print(f"ERROR: File not found: {c_code_path}")
        time.sleep(2)
        return
    
    folder = os.path.dirname(c_code_path)
    
    compiler_script = os.path.join(folder, "TINYCPU_compiler_in_python.py")
    assembler_script = os.path.join(folder, "TINYCPU_assembler_in_python.py")
    mac2mem_script = os.path.join(folder, "TINYCPU_mac2mem_in_python.py")
    
    for script in [compiler_script, assembler_script, mac2mem_script]:
        if not os.path.exists(script):
            print(f"ERROR: Script not found: {script}")
            print(f"Make sure all scripts are in the same folder as your C code: {folder}")
            time.sleep(2)
            return
    
    assembly_path = os.path.join(folder, "generated_assembly.txt")
    binary_path = os.path.join(folder, "generated_0and1s.txt")
    verilog_path = os.path.join(folder, "generated_mac2mem.txt")
    
    print("\n")
    print("-" * 100)
    print("TINYCPU Build Pipeline")
    print("-" * 100)
    print(f"Input C code: {c_code_path}")
    print(f"Output folder: {folder}")
    print("-" * 100)
    time.sleep(1.5)
    print("\n")
    
    print("STEP 1: Compiling C code to Assembly...")
    time.sleep(0.7)
    if not run_script_with_input(compiler_script, c_code_path):
        print("Build FAILED at compilation step")
        time.sleep(2)
        return
    
    if not os.path.exists(assembly_path):
        print(f"ERROR: Expected assembly file not found: {assembly_path}")
        time.sleep(2)
        return
    
    print("\n")
    time.sleep(0.7)
    
    print("STEP 2: Assembling to binary...")
    time.sleep(0.7)
    if not run_script_with_input(assembler_script, assembly_path):
        print("Build FAILED at assembly step")
        time.sleep(2)
        return
    
    if not os.path.exists(binary_path):
        print(f"ERROR: Expected binary file not found: {binary_path}")
        time.sleep(2)
        return
    
    print("\n")
    time.sleep(0.7)
    
    print("STEP 3: Converting to Verilog memory format...")
    time.sleep(0.7)
    if not run_script_with_input(mac2mem_script, binary_path):
        print("Build FAILED at mac2mem step")
        time.sleep(2)
        return
    
    if not os.path.exists(verilog_path):
        print(f"ERROR: Expected Verilog file not found: {verilog_path}")
        time.sleep(2)
        return
    
    print("\n")
    time.sleep(1)
    print("-" * 100)
    print("BUILD SUCCESSFUL!")
    print("-" * 100)
    time.sleep(0.7)
    print(f"Generated files:")
    time.sleep(0.5)
    print(f"  Assembly:  {assembly_path}")
    time.sleep(0.5)
    print(f"  Binary  :  {binary_path}")
    time.sleep(0.5)
    print(f"  Verilog :  {verilog_path}")
    time.sleep(0.7)
    print("-" * 100)
    time.sleep(2)

main()
#---------------------------------------------------------------------------------------------------------------------------
