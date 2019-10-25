"""CPU functionality."""

import sys
import binascii

LDI  = 0b10000010
PRN  = 0b01000111
HLT  = 0b00000001
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
ADD  = 0b10100000
RET  = 0b00010001
PRA  = 0b01001000
AND  = 0b10101000
XOR  = 0b10101011
NOP  = 0b00000000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = 7
        self.message = []

    def load(self, file):
        """Load a program into memory."""

        try:
            address = 0
            with open(file) as f:
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#")

                    # Convert any numbers from binary strings to integers
                    num = comment_split[0].strip()
                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue

                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):

        return self.ram[address]

    def ram_write(self, address, value):

        self.ram[address] = value

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
        """Run the CPU."""
        running = True

        while running:
    # Do stuff
            command = self.ram[self.pc]
            print(f'{command} and pc is {self.pc}')
            if command == LDI: #LDI, needs register and numer
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                self.pc += 3

            elif command == PRN: #PRN, needs register to print
                print(self.reg[self.ram[self.pc+1]])
                self.pc += 2

            elif command == HLT:
                running = False

            elif command == MUL:
                self.reg[self.ram[self.pc+2]]
                self.alu("MUL", self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc += 3
            
            elif command == ADD: 
                self.reg[self.ram[self.pc+1]] += self.reg[self.ram[self.pc+2]]
                self.pc += 1

            elif command == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # Decrement the SP.
                self.reg[self.sp] -= 1
                # Copy the value in the given self.reg to the address pointed to by self.sp.
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif command == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]
                # Copy the value from the address pointed to by self.sp to the given self.reg.
                self.reg[reg] = val
                # Increment self.sp.
                self.reg[self.sp] += 1
                self.pc += 2

            elif command == CALL:
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]

            elif command == PRA:
                reg = self.ram[self.pc + 1]
                self.message.append(chr(self.reg[reg]))
                self.pc += 2
            
            elif command == AND:
                self.reg[self.ram[self.pc + 1]] = self.reg[self.ram[self.pc + 1]] & self.reg[self.ram[self.pc + 2]]
                self.pc += 3

            elif command == XOR:
                self.reg[self.ram[self.pc + 1]] = self.reg[self.ram[self.pc + 1]] ^ self.reg[self.ram[self.pc + 2]]
                self.pc += 3

            elif command == NOP:
                self.pc += 1

               

            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)
        return self.message