import re
import subprocess
import opcodes

def rom_to_buffer(filename):
    dump = subprocess.run(['hexdump', filename], stdout=subprocess.PIPE).stdout.decode('utf-8')
    temp = re.sub(r'\w\w\w\w\w\w\w ?', '', dump).replace("\n"," ").split(" ")
    buffer = []
    for x in temp:
        if x != '':
            buffer.append(x)
    return buffer

def disassemble(filename, pc = int("200", 16)):
    buffer = rom_to_buffer(filename)
    for i in range(0, len(buffer), 2):
        if(i + 1 >= len(buffer)):
            print(hex(pc), buffer[i], "->","just one byte must be data")
            continue
        opcode = buffer[i] + buffer[i + 1]
        print(hex(pc), buffer[i], buffer[i + 1], "->",opcodes.get_instruction_from_opcode(opcode))
        pc += 1