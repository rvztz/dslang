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
        Symbols.EQ: lambda x,y: x == y,
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

    def getmv(self, addr: any) -> any:
        if type(addr).__name__ == 'int':
            val = self.mem.get_memval(addr)
            if type(val).__name__ == 'Reference':
                return self.mem.get_memval(val.v)
            return val
        return self.getmv(addr.v)

    def getlt(self, val: any) -> any:
        if val:
            return val.v
        return val

    def getvq(self, q: Quad):
        ql = self.getmv if type(q.l).__name__ in {'int', 'Reference'} else self.getlt 
        qr = self.getmv if type(q.r).__name__ in {'int', 'Reference'} else self.getlt
        qv = self.getmv if type(q.v).__name__ in {'int', 'Reference'} else self.getlt
        return ql(q.l), qr(q.r), qv(q.v)

    def exec_quads(self):
        while self.qidx < len(self.quads):
            currq = self.quads[self.qidx]
            l,r,v = self.getvq(currq)
            print(self.qidx, currq)
            #print(l,r,v)
            print('----------------')
            if currq.o == Symbols.ASGN:
                self.assign(l,r,v)
            elif op := self.operations.get(currq.o, None):
                res = op(l, r)
                if currq.o == Symbols.C_MULT:
                    print(currq.o, l, r, res)
                    print('---------------------')
                self.mem.set_memval(v, res)
                self.qidx += 1
            elif op := getattr(self, currq.o, None):
                op(l,r,v)
            else:
                raise SystemExit('ExecError :: Unsupported op')
    
    def goto(self, l, r, v):
        self.qidx = v

    def gotof(self, l, r, v):
        if r is None:
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
        if len(self.pjumps) > 1:
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
