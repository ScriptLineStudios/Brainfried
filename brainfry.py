#!/usr/bin/env python

import sys
import time
import os

MOVE_POINTER_RIGHT = ">"
MOVE_POINTER_LEFT = "<"
INCREMENT = "+"
DECREMENT = "-"
OUT = "."
IN = ","
OPEN_BRACKET = "["
CLOSE_BRACKET = "]"

INSTRUCTIONS = (MOVE_POINTER_LEFT, MOVE_POINTER_RIGHT, INCREMENT, DECREMENT, OPEN_BRACKET, CLOSE_BRACKET, OUT, IN)

optimize = True

def help():
    print("Usage:")
    print("    python brainfired.py [options] <brainfuck file to compile>:  Compiles brainfuck to assembly")
    print("    python brainfired.py --help:                                 Prints this message \n")
    print("Options: ")
    print("    -r:                Run the generated assembly using nasm.")
    print("    --dont-optimize:   Don't apply any optimizations. Warning: Can lead to slower exectuables but faster compile times")

def parse_repetitve_commands(program):
    groupings = []
    prev_op = None
    for ip, op in enumerate(program):
        if op == INCREMENT and prev_op != INCREMENT or op == DECREMENT and prev_op != DECREMENT:
            groupings.append([ip, 1])
        if prev_op == op:
            groupings[-1][1] += 1
            prev_op = op
    return dict(groupings)

def find_bracket_pairs(program):
    stack = []
    bracket_lookup = {}

    for ip, op in enumerate(program):
        if op == OPEN_BRACKET:
            stack.append(ip)
        elif op == CLOSE_BRACKET:
            ip_to_jump_to = stack.pop()

            bracket_lookup[ip_to_jump_to] = ip #Going from front to back
            bracket_lookup[ip] = ip_to_jump_to #Going from back to front

    return bracket_lookup

def generate_asm(program, out, bracket_lookup, groupings):
    instruction_pointer =  0
    while instruction_pointer < len(program):
        op = program[instruction_pointer]
        if op == MOVE_POINTER_RIGHT:
            out.write("    ;;move right\n")
            out.write("    sub rsp, 8\n")
        elif op == MOVE_POINTER_LEFT:
            out.write("    ;;move left\n")
            out.write("    add rsp, 8\n")
        elif op == INCREMENT:
            out.write("    ;;add\n")
            if optimize:
                if instruction_pointer in groupings:
                    amount = groupings[instruction_pointer]
                    out.write("    mov rax, [rsp]\n")
                    out.write(f"    add rax, {amount}\n")
                    out.write("    mov [rsp], rax\n")
            else:
                out.write("    mov rax, [rsp]\n")
                out.write("    inc rax\n")
                out.write("    mov [rsp], rax\n")
        elif op == DECREMENT:
            out.write("    ;;subtract\n")
            if optimize:
                if instruction_pointer in  groupings:
                    amount = groupings[instruction_pointer]
                    out.write("    mov rax, [rsp]\n")
                    out.write(f"    sub rax, {amount}\n")
                    out.write("    mov [rsp], rax\n")
            else:
                out.write("    mov rax, [rsp]\n")
                out.write("    dec rax\n")
                out.write("    mov [rsp], rax\n")
        elif op == OUT:
            out.write("    ;;out\n")
            out.write("    mov rax, [rsp]\n") 
            out.write("    mov rbx, rax\n")
            out.write("    mov [sum], rax\n")
            out.write("    mov rax, 1\n")
            out.write("    mov rdi, 1\n")
            out.write("    mov rsi, sum\n")
            out.write("    mov rdx, 1\n")
            out.write("    syscall\n")

        elif op == IN:
            out.write("    ;;input\n")
            out.write("    mov rax, 0\n")
            out.write("    mov rdi, 1\n")
            out.write("    mov rsi, input_data\n")
            out.write("    mov rdx, 1\n")
            out.write("    syscall\n")
            out.write("    mov rbx, [input_data]\n")
            out.write("    mov [rsp], rbx\n")

        elif op == OPEN_BRACKET:
            out.write(f"opening_bracket_{instruction_pointer}:\n")
            out.write("    mov rax, [rsp]\n")
            out.write("    test rax, rax\n")
            out.write(f"    jz closing_bracket_{bracket_lookup[instruction_pointer]}\n") #If rax (current cell) is 0, jump to the closing bracket

        elif op == CLOSE_BRACKET:
            out.write(f"closing_bracket_{instruction_pointer}:\n")
            out.write("    mov rax, [rsp]\n")
            out.write("    test rax, rax\n")
            out.write(f"    jnz opening_bracket_{bracket_lookup[instruction_pointer]}\n") #If rax (current cell) is 0, jump to the opening bracket

        instruction_pointer += 1

def compile(file_path, out_filename):
    with open(file_path, "r") as in_file:
        lines = in_file.readlines()
        with open(f"{out_filename}.asm", "w") as out:
            out.write("section .data\n")
            out.write("sum:\n")
            out.write("    db 0\n")

            out.write("section .bss\n")
            out.write("    input_data resb 1\n")

            out.write("section	.text \n")
            out.write("    global _start\n")
            out.write("_start:\n")

            out.write("    mov rax, 0\n")
            out.write("    mov [rsp], rax\n")

            program = []
            for line in lines:
                for op in line:
                    if op in INSTRUCTIONS:
                        program.append(op)

            if optimize:
                groupings = parse_repetitve_commands(program)
            else:
                groupings = None
            table = find_bracket_pairs(program)
            
            generate_asm(program, out, table, groupings)

            out.write("    mov rax, 60\n")
            out.write("    mov rdi, 0\n")
            out.write("    syscall\n")

def main():
    if (len(sys.argv) < 2):
        help()
    else:
        if sys.argv[1] == "--help":
            help()
            exit()

        if "--dont-optimize" in sys.argv:
            optimize = False

        file_path = sys.argv[-1]
        out_filename = file_path.split(".")[0]

        start_time = time.perf_counter() 
        compile(file_path, out_filename)
        print(f"[INFO]: Compilation finished in {time.perf_counter()-start_time} seconds.")
        print(f"[INFO]: Used optimizations = {optimize}")

        if "-r" in sys.argv:
            print(f"[INFO]: Assembling {out_filename}.asm:")
            os.system(f"nasm -f elf64 -o {out_filename}.o {out_filename}.asm")
            print(f"[INFO]: Linking {out_filename}.o:")
            os.system(f"ld -o {out_filename} {out_filename}.o")
            print(f"[INFO]: Running {out_filename}:")
            os.system(f"./{out_filename}")

            os.system(f"rm {out_filename}.o")

if __name__ == "__main__":
    main()




