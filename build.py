from ModIO import CwCheatIO
from struct import pack
from psp_ge_asm import Assembler
from subprocess import run

main_address = 0x8800FF0
vformat = '2H4B2hH2x'
vertices = [
    (0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 39, 254, 0x00),
    (0xFF, 0xFF, 0x00, 0x00, 0x00, 0xFF, 286, 264, 0x00),
    (0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF, 40, 255, 0x00),
    (0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 285, 263, 0x00)
]


def patch(file):
    file.seek(0x8800D00)
    for vert in vertices:
        file.write(pack(vformat, *vert))

    file.seek(0x8800D40)
    file.write(b'\xFF\xFF')

    a = Assembler()
    with open("src/hp_bar.gasm", "r") as src:
        a.read(src)

    file.seek(0x8800F00)
    
    file.write(a.assemble())

    run(['armips', 'src/main.asm'])
    file.seek(main_address)
    with open('out/main.bin', 'rb') as src:
        file.write(src.read())
    
    file.seek(0x88E6D64)
    file.write(pack('I', main_address // 4 | 0x0A000000))


if __name__ == "__main__":
    with open("out/cheat.txt", "w+") as fd, CwCheatIO(fd) as file:
        file.write("Monster HP Bar")
        add = file.file.tell()
        file.file.write(f'_L 0xE1NN00FF 0x10000d40\n')
        patch(file)
        file.file.seek(add)
        lines = len(file.file.readlines())
        file.file.seek(add)
        file.file.write(f'_L 0xE1{hex(lines).replace("0x", ""):0>2}00FF')
