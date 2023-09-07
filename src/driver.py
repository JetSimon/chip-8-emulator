from emulator import Emulator
import turtle
import disassembler

filename = "../roms/test_opcode.ch8"
font_filename = "../fonts/chip48font.txt"
print("Remember all values are in hex")

disassembler.disassemble(filename)

emulator = Emulator(filename, font_filename)
emulator.set_resolution_multiplier(10)

while emulator.running:
    emulator.emulate_step()
    if emulator.update_display_flag:
        emulator.update_display_flag = False
        emulator.print_screen()
