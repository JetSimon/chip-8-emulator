import sys
import opcodes 
from disassembler import rom_to_buffer
filename = "../roms/2-ibm-logo.ch8"

if(len(sys.argv) > 1 and sys.argv[1]):
    filename = sys.argv[1]

print("Trying to get instructions needed for " + filename)

instructions = set()

buffer = rom_to_buffer(filename)
for i in range(0, len(buffer), 2):
    if(i + 1 >= len(buffer)):
        continue
    opcode = buffer[i] + buffer[i + 1]

    inst = opcodes.get_instruction_type_from_opcode(opcode)
    if inst:
        instructions.add(inst)

print(sorted(instructions))