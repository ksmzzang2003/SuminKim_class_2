com = {
'NOP' : 0,   # nop
'MOV' : 1,   # mov
'ADD' : 2,   # add
'SUB' : 3,  # sub
'MUL' : 4,  # mul
'DIV' : 5,  # div
'AND' : 6,  # and
'OR' : 7 , # or
'NOT' : 8,  # not
'BWA' : 9,  # bitwise and
'BWO' : 10,  # bitwise or
'BWX' : 11,  # bitwise xor
'BWL' : 12,  # bitwise rot left
'BWR' : 13,  # bitwise rot right
'BWN' : 14,  # bitwise not
'JMP' : 15,  # jump
'JPZ' : 16,  # jump if zero
'JPN' : 17,  # jump if nonzero
'SAV' : 18,  # save data
'LOD' : 19,  # load data
'HLT' : 20,  # halt
'ADR' : 21,  # toggle addressing mode
}
class Processor:
    acc = 0
    pc = 0
    instr = None
    instr_pc = None
    indirect = False

    program = None
    data = []

    def __init__(self, memsize):
        self.data = [0 for i in range(memsize)]
        self.memsize = memsize

    def save(self, y):
        if y > self.memsize or y < 0:
            raise Exception("Memory access error")
        self.data[y] = self.acc
        return (self.acc, self.pc)

    def load(self, y):
        if y > self.memsize or y < 0:
            raise Exception("Memory access error")
        return (self.data[y], self.pc)

    def toggle_adr(self):
        self.indirect = not self.indirect
        return (self.acc, self.pc)

    def get_y(self, y):
        return y if self.indirect is False else self.data[y]

    instruction_set = [
         lambda self, acc, pc, y: (acc, pc),
         lambda self, acc, pc, y: (self.get_y(y), pc),
         lambda self, acc, pc, y: (acc + self.get_y(y), pc),
         lambda self, acc, pc, y: (acc - self.get_y(y), pc),
         lambda self, acc, pc, y: (acc * self.get_y(y), pc),
         lambda self, acc, pc, y: (acc / self.get_y(y), pc),
         lambda self, acc, pc, y: (acc and self.get_y(y), pc),
         lambda self, acc, pc, y: (acc or self.get_y(y), pc),
         lambda self, acc, pc, y: (not acc, pc),
         lambda self, acc, pc, y: (acc & self.get_y(y), pc),
         lambda self, acc, pc, y: (acc | self.get_y(y), pc),
         lambda self, acc, pc, y: (acc ^ self.get_y(y), pc),
         lambda self, acc, pc, y: (acc << self.get_y(y), pc),
         lambda self, acc, pc, y: (acc >> self.get_y(y), pc),
         lambda self, acc, pc, y: (~ acc, pc),
         lambda self, acc, pc, y: (acc, self.get_y(y)),
         lambda self, acc, pc, y: (acc, self.get_y(y)) if acc == 0 else (acc, pc),
         lambda self, acc, pc, y: (acc, self.get_y(y)) if acc != 0 else (acc, pc),
         lambda self, acc, pc, y: self.save(self.get_y(y)),
         lambda self, acc, pc, y: self.load(self.get_y(y)),
         lambda self, acc, pc, y: (acc, -2),
         lambda self, acc, pc, y: self.toggle_adr()
    ]
    def process_instruction(self, x, y):
        (self.acc, self.pc) = self.instruction_set[x](self, self.acc, self.pc, y)
        self.acc = int(self.acc)
        self.pc = int(self.pc) + 1

    def read_program(self, program):
        self.program = program

    def fetch_instruction(self):
        if self.instr_pc == self.pc:
            return self.instr
        self.instr_pc = self.pc
        if self.instr_pc < len(self.program):
            self.instr = self.program[self.instr_pc]
        else:
            raise Exception("Exceeded program code")
        return self.instr

    def execute_if_not_halted(self):
        if self.pc == -1:
            return True
        self.fetch_instruction()
        instr = self.instr
        self.process_instruction(instr[0], instr[1])
        return False
    def run(self):
        halted = False;
        while not halted:
            halted = self.execute_if_not_halted()
lines = []
while True:
    L = input().split('\n')[0]
    if L == 'QUIT':
        break
    elif L != '':
        lines.append(L)
cpu = Processor(100)
cpu.read_program([list(map(lambda l: com[l], line.split(" "))) for line in lines])
cpu.run()

print("CPU Memory data:", cpu.data)
print("Final accumulator value:", cpu.acc)