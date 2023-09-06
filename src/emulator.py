import disassembler
import opcodes

""" 
4K RAM - by convention programs start in RAM at 0x200

Display is 64x32 (1 bit per pixel).

Display buffer is in RAM at 0xF00.

Stack is at 0xEA0.

16 8-bit registers named V0, V1, V2, ... VF

A memory address register called I

Has stack instructions (so needs an SP)

2 timers, one for delay, and one for sound
"""

filename = "../roms/Fishie.ch8"

buffer = disassembler.rom_to_buffer(filename)

pc = int("200", 16)

print("Remember all values are in hex")

for i in range(0, len(buffer), 2):
    if(i == len(buffer) - 1 or buffer[i] == '' or buffer[i + 1] == ''):
        break
    opcode = buffer[i] + buffer[i + 1]
    print(hex(pc), buffer[i], buffer[i + 1], "->",opcodes.get_instruction_from_opcode(opcode))
    pc += 1