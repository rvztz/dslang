from typing import Deque
from collections import deque
from dslang.util.tokens import Symbols
from dslang.vm.mem import MemHandler
from dslang.lexpar.ctx import Quad

class QuadExecutor:
    
    operations = {
        Symbols.AND: lambda x,y: x and y,
        Symbols.C_OR: lambda x,y: x or y,
        Symbols.LT: lambda x,y: x < y,
        Symbols.GT: lambda x,y: x > y,
        Symbols.LTEQ: lambda x,y: x <= y,
        Symbols.GTEQ: lambda x,y: x >= y,
        Symbols.C_ADD: lambda x,y: x + y,
        Symbols.SUB: lambda x,y: x - y,
        Symbols.C_EXP: lambda x,y: x ** y,
        Symbols.C_MULT: lambda x,y: x * y,
        Symbols.DIV: lambda x,y: x / y
    }

    def __init__(self, mem: MemHandler, quads: Deque[Quad]) -> None:
        self.mem = mem
        self.quads = quads
        self.pjumps = deque()
        self.qidx = 0

    def exec_quads(self):
        while self.qidx < len(self.quads):
            currq = self.quads[self.qidx]
            if currq.o == Symbols.ASGN:
                self.assign(currq)
            elif op := self.operations.get(currq.o, None):
                val = self.mem.get_memval(currq.l)
                var = self.mem.get_memval(currq.r)
                if currq.literal:
                    res = op(val, currq.r)
                else: 
                    res = op(val, var)
                self.mem.set_memval(currq.v, res)
                self.qidx += 1
            elif op := getattr(self, currq.o, None):
                op(currq)
            else:
                raise SystemExit('ExecError :: Unsupported op')
    
    def goto(self, q: Quad):
        self.qidx = q.v

    def gotof(self, q: Quad):
        val = self.mem.get_memval(q.r)
        self.qidx = q.v if (not val) else self.qidx + 1

    def gotov(self, q: Quad):
        val = self.mem.get_memval(q.r)
        self.qidx = q.v if val else self.qidx + 1

    def gosub(self, q: Quad):
        self.pjumps.append(q.v)
        self.qidx = q.r

    def param(self, q: Quad):
        self.assign(q)

    def verif(self, q: Quad):
        val = self.mem.get_memval(q.l)
        if not (q.r <= val < q.v):
            raise SystemExit('IndexError :: Index out of bounds')
        self.qidx += 1

    def bfunc(self, q: Quad):
        return self.goto(q)

    def endfunc(self, q: Quad):
        if self.pjumps:
            self.qidx = self.pjumps.pop()
        else:
            self.qidx += 1

    def read(self, q: Quad):
        r = input('<|')
        if q.deref:
            addr = self.mem.get_memval(q.v)
            self.mem.set_memval(addr, r)
        else:
            self.mem.set_memval(q.v, r)
        self.qidx += 1

    def write(self, q: Quad):
        val = self.mem.get_memval(q.v)
        print(q.deref)
        if q.deref:
            val = self.mem.get_memval(val)
        print(f'|> {val}')
        self.qidx += 1

    def assign(self, q: Quad):
        val = self.mem.get_memval(q.r)
        if q.deref:
            addr = self.mem.get_memval(q.v)
            self.mem.set_memval(addr, val)
        else:
            self.mem.set_memval(q.v, val)
        self.qidx += 1
