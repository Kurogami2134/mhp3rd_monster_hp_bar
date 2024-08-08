.psp

sceGeListEnQueue equ 0x08960CF8

.createfile "out/main.bin", 0x8800FF0

    ; skip if not in quest
    li          a0, 0x09C57CA0
    lw          a0, 0x0(a0)
    li          a1, 0x656D6167
    bne         a0, a1, ret

    ; skip if returning

    li          a0, 0x09BAC044
    lb          a0, 0x0(a0)
    slti        at, a0, 0x3
    beq         at, zero, ret
    
    ; skip drawing in loading screens
    li          a0, 0x08AB49EC
    lb          a0, 0x0(a0)
    bne         a0, zero, ret

    li          a0, 0x9DA9860
    lw          a0, 0x0(a0)

    ; (mhp * 245 / mfhp) + 40

    lh          a1, 0x246(a0)
    li          a2, 245
    mult        a1, a2
    mflo        a1

    lh          a2, 0x288(a0)
    div         a1, a2
    mflo        a1
    addiu       a1, a1, 0x28

    li          a2, 0x8800d38
    sh          a1, 0x0(a2)

    ; queue rendering

    li          a0, 0x8800F00
    jal         sceGeListEnQueue
    li          a1, 0x0

ret:
    li          a0, 0x09ADB910
    li          a1, 0x0
    li          a2, 0x1
    li          ra, 0x088E6D6C
    j           0x088EBAB8
    nop

.close
