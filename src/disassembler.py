import re
import subprocess

def rom_to_buffer(filename):
    dump = subprocess.run(['hexdump', filename], stdout=subprocess.PIPE).stdout.decode('utf-8')
    temp = re.sub(r'\w\w\w\w\w\w\w ?', '', dump).replace("\n"," ").split(" ")
    buffer = []
    for x in temp:
        if x != '':
            buffer.append(x)
    return buffer