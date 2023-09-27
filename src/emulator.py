import disassembler
import opcodes
import os 
import serial
import time

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

DEBUG = False

class Emulator():
    def __init__(self, filename, font_filename, use_arduino=True):
        self.rom_filename = filename
        self.registers = {}
        for i in range(0, 16):
            self.registers[f"V{hex(i).split('x')[1]}"] = 0
        self.I = 0
        self.pc = int("200", 16)
        self.display_buffer = int("F00", 16)
        self.delay_timer = 0
        self.sound_timer = 0
        self.memory = [0] * 4096
        self.stack = [0] * 4096

        self.skip_flag = False
        self.running = True

        self.load_font(font_filename)
        self.load_into_memory()
        self.update_display_flag = True

        self.resolution_multiplier = 1

        self.pixels = []
        for y in range(32):
            self.pixels.append([0] * 64)

        self.use_arduino = use_arduino
        if use_arduino:
            self.arduino = serial.Serial(port='/dev/cu.usbmodem14501', baudrate=115200, write_timeout=0)

    def call(self, new):
        self.stack.append(self.pc)
        self.pc = new
    
    def ret(self):
        self.pc = self.stack.pop()

    def set_resolution_multiplier(self, n):
        self.resolution_multiplier = n

    def clear_screen(self):
        self.pixels = []
        for y in range(32):
            self.pixels.append([0] * 64)

        if self.use_arduino:
            self.arduino.write(bytes("clrscrn", 'utf-8'))
            time.sleep(0.01)

    def print_screen(self):
        os.system('clear')
        print(f"{self.registers}")
        for row in self.pixels:
            s = ""
            for pixel in row:
                s += "▓" if pixel != 0 else "░"
            print('\x1b[6;30;42m' + s + '\x1b[0m')

    def draw_pixel(self, x, y, on):
        if x < 0 or x >= len(self.pixels[0]) or y < 0 or y >= len(self.pixels):
            return
        self.pixels[y][x] = on ^ self.pixels[y][x]
        if self.use_arduino:
            toSend = str(x).ljust(3) + str(y).ljust(3) + ("1" if self.pixels[y][x] else "0")
            self.arduino.write(bytes(toSend, 'utf-8'))
            #print(f"sent {toSend} now sleep...")
            time.sleep(1)
            #print(self.arduino.readlines())
            #time.sleep(0.2)
    def skip_next_instruction(self):
        self.skip_flag = True

    def set_memory(self, index, value):
        self.memory[index] = self.get_real_value(value)

    def get_registers(self, a, b):
        return self.get_register(a), self.get_register(b)

    def get_register(self, key):
        return self.registers["V" + key]
    
    def set_flag(self, value):
        self.set_register("f", self.get_real_value(value))

    def set_register(self, key, value):
        self.registers["V" + key] = self.get_real_value(value)

    def get_real_value(self, value, bits=8):
        return int(bin(value).split("b")[1].zfill(bits)[-bits:], 2)

    def halt(self):
        self.running = False

    def load_font(self, font_filename):
        # Using readlines()
        f = open(font_filename, 'r')
        offset = 0
        # Strips the newline character
        for line in f.readlines():
            if "0b" not in line:
                continue
            self.memory[offset] = int(line, 2)
            #print(hex(self.memory[offset]))
            offset += 1
        f.close()

    def load_into_memory(self):
        buffer = disassembler.rom_to_buffer(self.rom_filename)
        offset = 0
        for i in range(0, len(buffer)):
            self.memory[self.pc + offset] = int(buffer[i], 16)
            offset += 1
    
    def emulate_step(self):
        opcode = opcodes.dec_to_hex_byte(self.memory[self.pc]) + opcodes.dec_to_hex_byte(self.memory[self.pc + 1])

        if(DEBUG):
            print("attempting", opcode, "=>", opcodes.get_instruction_from_opcode(opcode))
        
        self.pc += 2
        opcodes.apply_instruction_from_opcode(opcode, self)

        if(DEBUG):
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

            


