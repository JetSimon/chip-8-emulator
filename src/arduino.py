import disassembler
import sys

filename = "../roms/2-ibm-logo.ch8"

if(len(sys.argv) > 1 and sys.argv[1]):
    filename = sys.argv[1]

print("Trying to convert " + filename)

bytes = disassembler.rom_to_buffer(filename)

for i in range(len(bytes)):
    bytes[i] = "0x" + bytes[i]

print("#define ROM " + str(bytes).replace("'", "").replace("[","").replace("]",""))