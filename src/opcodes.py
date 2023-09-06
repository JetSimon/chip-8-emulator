import re

def get_instruction_from_opcode(opcode):
    if re.match(r"00EE", opcode):
        return "Return"
    elif re.match(r"00E0", opcode):
        return "Clear Display"
    elif re.match(r"0\w\w\w", opcode):
        return f"Call machine code routine at address {opcode[1:]}"
    elif re.match(r"1\w\w\w", opcode):
        return f"Jump to address {opcode[1:]}"
    elif re.match(r"2\w\w\w", opcode):
        return f"Call subroutine at {opcode[1:]}"
    elif re.match(r"3\w\w\w", opcode):
        return f"if (V{opcode[1]} == {opcode[2:]})"
    elif re.match(r"4\w\w\w", opcode):
        return f"if (V{opcode[1]} != {opcode[2:]})"
    elif re.match(r"5\w\w0", opcode):
        return f"if (V{opcode[1]} == {opcode[2]})"
    elif re.match(r"6\w\w\w", opcode):
        return f"V{opcode[1]} = {opcode[2:]}"
    elif re.match(r"7\w\w\w", opcode):
        return f"V{opcode[1]} += {opcode[2:]}"
    elif re.match(r"8\w\w0", opcode):
        return f"V{opcode[1]} = {opcode[2]}"
    elif re.match(r"8\w\w1", opcode):
        return f"V{opcode[1]} |= {opcode[2]}"
    elif re.match(r"8\w\w2", opcode):
        return f"V{opcode[1]} &= {opcode[2]}"
    elif re.match(r"8\w\w3", opcode):
        return f"V{opcode[1]} ^= {opcode[2]}"
    elif re.match(r"8\w\w4", opcode):
        return f"V{opcode[1]} += {opcode[2]}"
    elif re.match(r"8\w\w5", opcode):
        return f"V{opcode[1]} -= {opcode[2]}"
    elif re.match(r"8\w\w6", opcode):
        return f"V{opcode[1]} >>= {opcode[2]}"
    elif re.match(r"8\w\w7", opcode):
        return f"V{opcode[1]} = {opcode[2]} - V{opcode[1]}"
    elif re.match(r"8\w\wE", opcode):
        return f"V{opcode[1]} <<= 1"
    elif re.match(r"9\w\w0", opcode):
        return f"if (V{opcode[1]} != {opcode[2:]}) then SKIP"
    elif re.match(r"a\w\w\w", opcode):
        return f"I = {opcode[1:]}"
    elif re.match(r"b\w\w\w", opcode):
        return f"PC = V0 + {opcode[1:]}"
    elif re.match(r"c\w\w\w", opcode):
        return f"V{opcode[1]} = rand(0, 255) & {opcode[2:]}"
    elif re.match(r"d\w\w\w", opcode):
        return f"draw(V{opcode[1]}, V{opcode[2], {opcode[3]}}) - See wikipedia"
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