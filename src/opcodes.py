import re
import random 

def dec_to_hex_byte(dec):
    return hex(dec).split("x")[1].zfill(2)

def apply_instruction_from_opcode(opcode, emulator):

    if(type(opcode) is not str):
        print("Error: expected opcode instead got", opcode)
        emulator.halt()
        return

    if re.match(r"00ee", opcode):
        emulator.ret()
    elif re.match(r"00e0", opcode):
        emulator.clear_screen()
    elif re.match(r"0\w\w\w", opcode):
        n = int(opcode[1:], 16)
        emulator.call(n)
    elif re.match(r"1\w\w\w", opcode):
        emulator.pc = int(opcode[1:], 16)
    elif re.match(r"2\w\w\w", opcode):
        n = int(opcode[1:], 16)

        if(n >= len(emulator.memory)):
           print(f"Error: trying to access address outside of memory ({n},{hex(n)})")
           emulator.halt()
           return
        emulator.call(emulator.memory[n])
    elif re.match(r"3\w\w\w", opcode):
        x = emulator.get_register(opcode[1])
        n = int(opcode[2:],16)
        if(x == n):
            emulator.skip_next_instruction()
    elif re.match(r"4\w\w\w", opcode):
        x = emulator.get_register(opcode[1])
        n = int(opcode[2:],16)
        if(x != n):
            emulator.skip_next_instruction()
    elif re.match(r"5\w\w0", opcode):
        x, y = emulator.get_registers(opcode[1], opcode[2])
        if(x == y):
            emulator.skip_next_instruction()
    elif re.match(r"6\w\w\w", opcode):
        emulator.set_register(opcode[1], int(opcode[2:], 16))
    elif re.match(r"7\w\w\w", opcode):
        x = emulator.get_register(opcode[1])
        emulator.set_register(opcode[1], x + int(opcode[2:], 16))
    elif re.match(r"8\w\w0", opcode):
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], y)
    elif re.match(r"8\w\w1", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x | y)
    elif re.match(r"8\w\w2", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x & y)
    elif re.match(r"8\w\w3", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x ^ y)
    elif re.match(r"8\w\w4", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x + y)
        emulator.set_flag(1 if x + y > 15 else 0)
    elif re.match(r"8\w\w5", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x - y)
        emulator.set_flag(0 if x + y > 15 else 1)
    elif re.match(r"8\w\w6", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x >> 1)
        emulator.set_flag(x & 1)
    elif re.match(r"8\w\w7", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], y - x)
        emulator.set_flag(1 if x + y > 15 else 0)
    elif re.match(r"8\w\wE", opcode):
        x = emulator.get_register(opcode[1])
        y = emulator.get_register(opcode[2])
        emulator.set_register(opcode[1], x << 1)
        emulator.set_flag(msb(x))
    elif re.match(r"9\w\w0", opcode):
        x, y = emulator.get_registers(opcode[1], opcode[2])
        print(x,y)
        if(x != y):
            emulator.skip_next_instruction()
    elif re.match(r"a\w\w\w", opcode):
        n = int(opcode[1:], 16)
        emulator.I = n
    elif re.match(r"b\w\w\w", opcode):
        n = int(opcode[1:], 16)
        emulator.pc = emulator.get_register(0) + n
    elif re.match(r"c\w\w\w", opcode):
        n = int(opcode[2:], 16)
        res = random.randint(0, 255) & n
        emulator.set_register(opcode[1], res)
    elif re.match(r"d\w\w\w", opcode):
        x1 = emulator.get_register(opcode[1])
        y1 = emulator.get_register(opcode[2])
        N = int(opcode[3], 16)
        I = emulator.I
        for y in range(0, N):
            byte = emulator.memory[I + y]
            x = 0
            bits = bin(byte).split("b")[1].zfill(8)
            for bit in bits:
                emulator.draw_pixel(x1+x, y1+y, int(bit))
                x += 1
        emulator.update_display_flag = True
    elif re.match(r"e\w9e", opcode):
        skip = random.randint(0,1) == 0
        print(f"Would skip if key in V{opcode[1]} is pressed, random:", skip)
        if skip:
            emulator.skip_next_instruction()
    elif re.match(r"e\wa1", opcode):
        skip = random.randint(0,1) == 0
        print(f"Would skip if key in V{opcode[1]} is not pressed, random:", skip)
        if skip:
            emulator.skip_next_instruction()
    elif re.match(r"f\w07", opcode):
        emulator.set_register(opcode[1], emulator.delay_timer)
    elif re.match(r"f\w0a", opcode):
        emulator.set_register(opcode[1], emulator.sound_timer)
    elif re.match(r"f\w15", opcode):
        n = int(opcode[1], 16)
        emulator.delay_timer = n
    elif re.match(r"f\w18", opcode):
        n = int(opcode[1], 16)
        emulator.sound_timer = n
    elif re.match(r"f\w1e", opcode):
        emulator.I += emulator.get_register(opcode[1])
    elif re.match(r"f\w29", opcode):
        loc = int(opcode[1], 16) * 5
        #print("Would set I to sprite address for char " + opcode[1] + " = " + str(loc))
        emulator.I = emulator.memory[loc]
    elif re.match(r"f\w33", opcode):
        value = emulator.get_register(opcode[1])
        ones = value % 10
        value = value / 10
        tens = value % 10
        hundreds = value / 10
        emulator.memory[emulator.I] = hundreds
        emulator.memory[emulator.I + 1] = tens
        emulator.memory[emulator.I + 2] = ones
    elif re.match(r"f\w55", opcode):
        x = int(opcode[1], 16)

        offset = 0
        for n in range(x):
            key = "V" + hex(n).split("x")[1]
            emulator.memory[emulator.I + offset] = emulator.registers[key]
            offset += 1
    elif re.match(r"f\w65", opcode):
        x = opcode[1]
        n = int(x, 16)

        offset = 0
        for y in range(0, n + 1):
            h = hex(y).split('x')[1]
            key = "V" + h
            emulator.registers[key] = emulator.memory[emulator.I + offset]
            offset += 1
    else:
        print("Unimplemented:", opcode, emulator.halt())

def get_instruction_from_opcode(opcode):
    if re.match(r"00ee", opcode):
        return "Return"
    elif re.match(r"00e0", opcode):
        return "Clear Display"
    elif re.match(r"0\w\w\w", opcode):
        return f"Call machine code routine at address {opcode[1:]}"
    elif re.match(r"1\w\w\w", opcode):
        return f"Jump to address {opcode[1:]}"
    elif re.match(r"2\w\w\w", opcode):
        return f"Call subroutine at {opcode[1:]}"
    elif re.match(r"3\w\w\w", opcode):
        return f"if (V{opcode[1]} == {int(opcode[2:], 16)})"
    elif re.match(r"4\w\w\w", opcode):
        return f"if (V{opcode[1]} != {int(opcode[2:], 16)})"
    elif re.match(r"5\w\w0", opcode):
        return f"if (V{opcode[1]} == V{opcode[2]})"
    elif re.match(r"6\w\w\w", opcode):
        return f"V{opcode[1]} = {int(opcode[2:], 16)}"
    elif re.match(r"7\w\w\w", opcode):
        return f"V{opcode[1]} += {int(opcode[2:], 16)}"
    elif re.match(r"8\w\w0", opcode):
        return f"V{opcode[1]} = {int(opcode[2], 16)}"
    elif re.match(r"8\w\w1", opcode):
        return f"V{opcode[1]} |= {int(opcode[2], 16)}"
    elif re.match(r"8\w\w2", opcode):
        return f"V{opcode[1]} &= {int(opcode[2], 16)}"
    elif re.match(r"8\w\w3", opcode):
        return f"V{opcode[1]} ^= {int(opcode[2], 16)}"
    elif re.match(r"8\w\w4", opcode):
        return f"V{opcode[1]} += {int(opcode[2], 16)}"
    elif re.match(r"8\w\w5", opcode):
        return f"V{opcode[1]} -= {int(opcode[2], 16)}"
    elif re.match(r"8\w\w6", opcode):
        return f"V{opcode[1]} >>= {int(opcode[2], 16)}"
    elif re.match(r"8\w\w7", opcode):
        return f"V{opcode[1]} = {int(opcode[2], 16)} - V{opcode[1]}"
    elif re.match(r"8\w\wE", opcode):
        return f"V{opcode[1]} <<= 1"
    elif re.match(r"9\w\w0", opcode):
        return f"if (V{opcode[1]} != {opcode[2]}) then SKIP"
    elif re.match(r"a\w\w\w", opcode):
        return f"I = {int(opcode[1:], 16)}"
    elif re.match(r"b\w\w\w", opcode):
        return f"PC = V0 + {int(opcode[1], 16)}"
    elif re.match(r"c\w\w\w", opcode):
        return f"V{opcode[1]} = rand(0, 255) & {opcode[2:]}"
    elif re.match(r"d\w\w\w", opcode):
        return f"draw(V{opcode[1]}, V{opcode[2]}, {opcode[3]}) - See wikipedia"
    elif re.match(r"e\w9e", opcode):
        return f"if(key in V{opcode[1]} pressed)"
    elif re.match(r"e\wa1", opcode):
        return f"if(key in V{opcode[1]} not pressed)"
    elif re.match(r"f\w07", opcode):
        return f"V{opcode[1]} = delay timer value"
    elif re.match(r"f\w0a", opcode):
        return f"V{opcode[1]} = blocking wait for key press"
    elif re.match(r"f\w15", opcode):
        return f"Set delay timer to V{opcode[1]}"
    elif re.match(r"f\w18", opcode):
        return f"Set sound timer to V{opcode[1]}"
    elif re.match(r"f\w1e", opcode):
        return f"I += V{opcode[1]}"
    elif re.match(r"f\w29", opcode):
        return f"I = sprite_addr[V{opcode[1]}]"
    elif re.match(r"f\w33", opcode):
        return f"BCD with V{opcode[1]} hopefully we don't need this?"
    elif re.match(r"f\w55", opcode):
        return f"reg_dump(V{opcode[1]}, &I)"
    elif re.match(r"f\w65", opcode):
        return f"reg_load(V{opcode[1]}, &I)"
    else:
        return "Invalid instruction? Could be data"
    
def binary(i):
    if i == 0:
        return "0"
    s = ''
    while i:
        if i & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        i >>= 1
    return s 

def msb(i):
    a = binary(i)
    b = a[0:7]   # gets first SEVEN characters of string a
    c = int(b,2)
    return c