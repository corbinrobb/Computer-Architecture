"""CPU functionality."""

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = False
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.stack_pointer = 255
        self.ops = {}
        self.ops[LDI] = self.LDI
        self.ops[PRN] = self.PRN
        self.ops[ADD] = self.ADD
        self.ops[MUL] = self.MUL
        self.ops[HLT] = self.HLT
        self.ops[PUSH] = self.PUSH
        self.ops[POP] = self.POP
        self.ops[CALL] = self.CALL
        self.ops[RET] = self.RET

    def LDI(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.ram_write(address, value)
        self.pc += 3

    def PRN(self):
        address = self.ram[self.pc + 1]
        self.ram_read(address)
        self.pc += 2
    
    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('ADD', reg_a, reg_b)
        self.pc += 3

    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def HLT(self):
        self.running = False

    def PUSH(self):
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = value
        self.pc += 2

    def POP(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.stack_pointer]
        self.reg[address] = value
        self.stack_pointer += 1
        self.pc += 2

    def CALL(self):
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = self.pc + 2
        self.pc = value

    def RET(self):
        address = self.ram[self.stack_pointer]
        self.stack_pointer += 1
        self.pc = address

    def ram_read(self, address):
        print(self.reg[address])

    def ram_write(self, address, value):
        self.reg[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            return

        path = sys.argv[1]

        with open('./examples/' + path) as f:
            lines = f.readlines()

        program = []

        for line in lines:
            line = line.strip()
            if '#' in line:
                comment_start = line.index('#')
                if comment_start == 0:
                    continue
                else:
                    binary = int(line[:comment_start].strip(), 2)
                    program.append(binary)
            elif line:
                binary = int(line, 2)
                program.append(binary)

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        self.running = True

        while self.running:
            ir = self.ram[self.pc]
            self.ops[ir]()
