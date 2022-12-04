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
        Symbols.NOTEQ: lambda x,y: x != y,
        Symbols.EQ: lambda x,y: x == y,
        Symbols.C_ADD: lambda x,y: x + y,
        Symbols.SUB: lambda x,y: x - y,
        Symbols.C_EXP: lambda x,y: x ** y,
        Symbols.C_MULT: lambda x,y: x * y,
        Symbols.DIV: lambda x,y: x / y,
        Symbols.FDIV: lambda x,y: x//y
    }

    def __init__(self, mem: MemHandler, quads: Deque[Quad], debug: False) -> None:
        self.mem = mem
        self.quads = quads
        self.pjumps = deque()
        self.qidx = 0
        self.debug = debug

    def getmv(self, addr: any) -> any:
        if (type(addr).__name__ == 'Literal') or (addr is None):
            return addr
        if (type(addr).__name__ == 'Reference'):
            ref = self.mem.get_memval(addr)
            refval = self.mem.get_memval(ref)
            while (type(refval).__name__ == 'Reference'): refval = self.mem.get_memval(refval)
            return refval
        return self.mem.get_memval(addr)
        

    def getlt(self, val: any) -> any:
        return val

    def getvq(self, q: Quad):
        return self.getmv(q.l), self.getmv(q.r), self.getmv(q.v)

    def exec_quads(self):
        while self.qidx < len(self.quads):
            currq = self.quads[self.qidx]
            l,r,v = self.getvq(currq)
            if self.debug:
                print(f'{self.qidx} :: {currq.o} | {l} | {r} | {v}')
            if currq.o == Symbols.ASGN:
                self.assign(l,r,v)
            elif op := self.operations.get(currq.o, None):
                res = op(l, r)
                self.mem.set_memval(v, res)
                self.qidx += 1
            elif op := getattr(self, currq.o, None):
                op(l,r,v)
            else:
                raise SystemExit('ExecError :: Unsupported op', currq.o)
    
    def goto(self, l, r, v):
        self.qidx = v

    def gotof(self, l, r, v):
        if r is None:
            print(l,r,v)
            raise SystemExit('Undefined.')
        self.qidx = v if (not r) else self.qidx + 1

    def gotov(self, l, r, v):
        self.qidx = v if r else self.qidx + 1

    def gosub(self, l, r, v):
        self.pjumps.append(v)
        self.qidx = r

    def param(self, l, r, v):
        self.assign(l,r,v)

    def verif(self, l, r, v):
        if not (r <= l < v):
            raise SystemExit('IndexError :: Index out of bounds')
        self.qidx += 1

    def bfunc(self, l, r, v):
        return self.goto(l,r,v)

    def endfunc(self, l, r, v):
        if len(self.pjumps) >= 1:
            self.qidx = self.pjumps.pop()
        else:
            self.qidx += 1

    def retfunc(self, l, r, v):
        self.mem.set_memval(v, r)
        self.endfunc(l,r,v)

    def read(self, l, r, v):
        r = input('<|')
        self.mem.set_memval(v, r)
        self.qidx += 1

    def write(self, l, r, v):
        print(f'|> {v}')
        self.qidx += 1

    def assign(self, l, r, v):
        self.mem.set_memval(v, r)
        self.qidx += 1
