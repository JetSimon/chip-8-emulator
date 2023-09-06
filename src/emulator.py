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

DEBUG = True

class Emulator():
    def __init__(self, filename):
        self.rom_filename = filename
        self.registers = {}
        for i in range(0, 16):
            self.registers[f"V{hex(i).split('x')[1]}"] = 0
        self.I = 0
        self.sp = int("EA0", 16)
        self.pc = int("200", 16)
        self.display_buffer = int("F00", 16)
        self.delay_timer = 0
        self.sound_timer = 0
        self.memory = [0] * 4096

        self.skip_flag = False
        self.running = True

        self.load_into_memory()

        self.resolution_multiplier = 1

        self.pixels = []
        for y in range(32):
            self.pixels.append([0] * 64)

    def call(self, new):
        self.memory[self.sp] = self.pc
        self.sp -= 1
        self.pc = new
    
    def ret(self):
        self.pc = self.memory[self.sp]
        self.sp += 1

    def set_resolution_multiplier(self, n):
        self.resolution_multiplier = n

    def clear_screen(self):
        self.pixels = []
        for y in range(32):
            self.pixels.append([0] * 64)

    def print_screen(self):
        for row in self.pixels:
            print(row)

    def draw_pixel(self, x, y):
        if x < 0 or x > len(self.pixels[0]) or y < 0 or x > len(self.pixels):
            return
        self.pixels[y][x] = 1

    def skip_next_instruction(self):
        self.skip_flag = True

    def get_registers(self, a, b):
        return self.get_register(a), self.get_register(b)

    def get_register(self, key):
        return self.registers["V" + key]
    
    def set_flag(self, value):
        self.set_register("f", value)

    def set_register(self, key, value):
        self.registers["V" + key] = value

    def halt(self):
        self.running = False

    def load_into_memory(self):
        buffer = disassembler.rom_to_buffer(self.rom_filename)
        offset = 0
        for i in range(0, len(buffer)):
            self.memory[self.pc + offset] = int(buffer[i], 16)
            offset += 1
    
    def emulate_step(self):
        opcode = opcodes.dec_to_hex_byte(self.memory[self.pc]) + opcodes.dec_to_hex_byte(self.memory[self.pc + 1])
        print("attempting", opcode, "=>", opcodes.get_instruction_from_opcode(opcode))
        
        self.pc += 2
        opcodes.apply_instruction_from_opcode(opcode, self)

        print("\n")
        print(self.registers, "\nI =", self.I)
        print("\n")

        if(not self.running):
            return

        if(self.skip_flag):
            self.pc += 2
            self.skip_flag = False
        
    def emulate(self):
        while(self.running):
            self.emulate_step()

            


