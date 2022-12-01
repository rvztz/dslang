from psutil import virtual_memory
from dslang.util.tokens import Reserved

def compute_block_size() -> int:
    disp = int(virtual_memory().available)//(100_000)
    return (disp - (disp%100)) // 20

class ReadOnlyProperty(Exception):
    def __init__(self) -> None:
        self.msg = 'Re-setting value after instantiation is not allowed.'
        super().__init__(self.msg)
    
class MemHandler:
    #BLOCK_SIZE = compute_block_size()
    BLOCK_SIZE = 2000
    TIDS = {Reserved.TINT:0, Reserved.TFLT:1, Reserved.TSTR:2, Reserved.TBOOL:3}
    SCOPE = {'global':0, 'function':1, 'local':2, 'const':3, 'temporal':4}
    def __init__(self) -> None:
        self.memdir = [[[0, [None] * self.BLOCK_SIZE] for _ in range(len(self.TIDS))] for _ in range(len(self.SCOPE))]

    def validate_memblock(self, scope: int, tid: int) -> bool:
        return self.memdir[scope][tid][0] < (self.BLOCK_SIZE)

    @staticmethod
    def translate_addr(addr: int) -> tuple:
        scope = (addr // 10_000)
        tid = (addr - (10_000 * scope)) // 1_000
        maddr = addr - (((scope*10)+tid) *1_000)
        scope, tid = scope-1, tid-1
        return scope, tid, maddr

    def get_vcount(self, scope: int, tid: int) -> int:
        return self.memdir[scope][tid][0]

    def alloc(self, sid: str, tid: int, size: int = None) -> int:
        scope = self.SCOPE[sid]
        tid = self.TIDS[tid]
        if not self.validate_memblock(scope, tid):
            raise Exception(f'DSLang error => Memory block full for scope_id/type_id: {scope},{tid}')
        addr = ((scope+1) * 10_000) + ((tid+1)*1_000) + self.memdir[scope][tid][0]
        increment = 1 if (size is None) else size
        self.memdir[scope][tid][0] += increment
        return addr

    def dealloc(self, addr: int) -> any:
        scope,tid,maddr = self.translate_addr(addr)
        self.memdir[scope][tid][1][maddr] = None
        self.memdir[scope][tid][0] -= 1

    def get_memval(self, addr: int) -> any:
        scope,tid,maddr = self.translate_addr(addr)
        return self.memdir[scope][tid][1][maddr]

    def set_memval(self, addr: int, value: any):
        scope,tid,maddr = self.translate_addr(addr)
        self.memdir[scope][tid][1][maddr] = value
    
    def reset(self, scope: int):
        self.memdir[scope] = [[0, [None] * self.BLOCK_SIZE] for _ in range(len(self.TIDS))]
