from emulator import Emulator
import turtle
import disassembler

filename = "../roms/Maze (alt) [David Winter, 199x].ch8"
print("Remember all values are in hex")

disassembler.disassemble(filename)

emulator = Emulator(filename)
emulator.set_resolution_multiplier(10)

while emulator.running:
    emulator.print_screen()
    emulator.emulate_step()
    input()
