from collections import deque
from dslang.util.dirs import FuncDir, ConstTab
from dslang.util.scube import SemanticCube
from dslang.util.tokens import Reserved
from dslang.vm.mem import MemHandler

class Quad:
    def __init__(self, op, loperand = None, roperand = None, 
                value = None, deref = None, literal = None) -> None:
        self.o = op
        self.l = loperand
        self.r = roperand
        self.v = value
        self.deref = deref
        self.literal = literal

    def __repr__(self) -> str:
        return f'{self.o} | {self.l} | {self.r} | {self.v}'

class ExprHelper:

    def __init__(self) -> None:
        self.operand_ctx = [deque()]
        self.operator_ctx = [deque()]

    @property
    def curr_operand_st(self):
        return self.operand_ctx[-1]

    @property
    def curr_operator_st(self):
        return self.operator_ctx[-1]

    def add_operand(self, pid, ptype, ref = False):
        self.curr_operand_st.append(dict(pid=pid, ptype =ptype, ref=ref))

    def create_operand_ctx(self):
        self.operand_ctx.append(deque())
        self.operator_ctx.append(deque())

    def pop_operand_ctx(self):
        prev_operand = self.operand_ctx.pop()
        prev_operator = self.operator_ctx.pop()
        self.operand_ctx[-1] += prev_operand
        self.operator_ctx[-1] += prev_operator


class ParsingScope:
    GLOBAL = 'global'
    FUNCTION = 'function'
    LOCAL = 'local'

class ParsingCtx:
    
    p_id: str = ''
    curr_vtype: str = ''
    curr_vid: str = ''
    curr_qidx : int = 0
    curr_dim: int = 1

    def __init__(self):
        self.funcdir = FuncDir()
        self.consts = ConstTab()
        self.mem = MemHandler()
        self.egen = ExprHelper()
        self.scube = SemanticCube()
        self.pscope = deque()
        self.func_ctx = deque()
        self.print_items = deque()
        self.pquads = deque()
        self.idx_agg = deque()
        self.quads = deque()

    @property
    def curr_fctx(self):
        return self.func_ctx[-1]

    @property
    def curr_pscope(self):
        return self.pscope[-1]
    
    @property
    def curr_func(self):
        return self.funcdir.get(self.curr_fctx)

    @property
    def mtid(self):
        return self.mem.TIDS.get(self.curr_vtype)

    @property
    def toperator(self):
        if self.egen.curr_operator_st:
            return self.egen.curr_operator_st[-1]
        return None
    
    def add_quad(self, op, l, r, v, deref = None, literal = None):
        self.quads.append(Quad(op, l, r, v, deref, literal))
        self.curr_qidx = len(self.quads)-1

    def update_quad(self, idx, **kwargs):
        quad = self.quads[idx]
        for k,v in kwargs.items():
            setattr(quad, k, v)
        self.quads[idx] = quad

    def add_fctx(self, fid):
        self.func_ctx.append(fid)
    
    def pop_fctx(self):
        self.func_ctx.pop()

    def add_pquad(self, idx):
        self.pquads.append(idx)

    def pop_pquad(self):
        return self.pquads.pop()

    def set_pscope(self, scope):
        if scope == ParsingScope.LOCAL:
            self.curr_func.add_auxvtab()
        self.pscope.append(scope)

    def reset_pscope(self):
        if self.curr_pscope == ParsingScope.LOCAL:
            self.curr_func.pop_auxvtab()
        self.pscope.pop()
       
    def cleanup_tmem(self, addrs: list):
        for addr in addrs:
            scope, _, _ = self.mem.translate_addr(addr)
            if scope == self.mem.SCOPE['temporal']:
                self.mem.dealloc(addr)      
    
    def add_var(self, varid: str, vtype: str, addr: int, lims: list = None):
        if self.curr_pscope == ParsingScope.GLOBAL:
            self.funcdir.get(self.p_id).vtab.add(varid, vtype, addr, lims)
        elif self.curr_pscope == ParsingScope.FUNCTION:
            self.curr_func.vtab.add(varid, vtype, addr, lims)
        elif self.curr_pscope == ParsingScope.LOCAL:
            self.curr_func.curr_auxvtab.add(varid, vtype, addr, lims)

    def update_var(self, varid: str, **kwargs):
        if self.curr_pscope == ParsingScope.GLOBAL:
            self.funcdir.get(self.p_id).vtab.update(varid, **kwargs)
        elif self.curr_pscope == ParsingScope.FUNCTION:
            self.curr_func.vtab.update(varid, **kwargs)
        elif self.curr_pscope == ParsingScope.LOCAL:
            self.curr_func.curr_auxvtab.update(varid, **kwargs)

    def get_var(self, varid):
        if self.curr_pscope == ParsingScope.GLOBAL:
            glb = self.funcdir.get(self.p_id).vtab.get(varid)
            var = glb
        else:
            var = self.curr_func.get_var(varid)
            glb = self.funcdir.get(self.p_id).vtab.get(varid)
            var = var or glb
        if var:
            return var
        raise Exception('VarID Error :: variable not declared')


    def deref_oper(self, oper):
        if oper['ref'] == False:
            return oper
        return dict(pid=self.mem.get_memval(oper['pid']), ptype=oper['ptype'])


    def gen_expr(self):
        roper, loper = self.egen.curr_operand_st.pop(), self.egen.curr_operand_st.pop()
        roper, loper = self.deref_oper(roper), self.deref_oper(loper) 
        operator = self.egen.curr_operator_st.pop()
        oper_type = self.scube.get(loper['ptype'], roper['ptype'], operator)
        if not oper_type:
            raise Exception(f'TypeError :: operation {operator} not allowed between types {loper["ptype"]}-{roper["ptype"]}')
        print(f'expr: = {loper["pid"]} || ', operator, f' || {roper["pid"]}')
        taddr = self.mem.alloc('temporal', self.mem.TIDS.get(oper_type))
        self.add_quad(operator, loper['pid'], roper['pid'], taddr)
        self.egen.add_operand(taddr, oper_type)
        #self.cleanup_tmem([loper['pid'], roper['pid']])

    def gen_print_quads(self):
        for addr in self.print_items:
            self.add_quad(Reserved.PRINT, None, None, addr)
        self.print_items.clear()

    def clean_function_mem(self):
        addresses = self.curr_func.dump_addr()
        for addr in addresses:
            self.mem.dealloc(addr)