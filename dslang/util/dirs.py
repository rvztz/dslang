from dslang.util.tokens import Reserved
class ExistingRow(Exception):
    def __init__(self, id) -> None:
        self.msg = f'Variable {id} already exists'
        super().__init__(self.msg)

class NonExistentRow(Exception):
    def __init__(self, id) -> None:
        self.msg = f'Variable {id} not declared'
        super().__init__(self.msg)

class Variable:
    def __init__(self, addr: int, vtype: str, limits: list) -> None:
        self.addr = addr
        self.vtype = vtype
        self.limits = [] if limits else limits
        self.is_array = True if limits else False
        self.size = 0 if limits else None
        self.r = 1 if limits else None
        if limits:
            self.add_dim(limits)

    def __repr__(self) -> str:
        return f'{self.addr} | {self.vtype} | {self.limits} | {self.size}'

    def validate_idx(self, idx, dim) -> bool:
        if self.is_array:
            return (idx >= 0) and (idx < self.limits[dim][1])
        return False

    def add_dim(self, dim: list):
        self.limits.append(dim)
        self.r = dim[1] * self.r

    def set_mdim(self):
        self.size = self.r
        for lim in self.limits:
            mdim = self.r // lim[1]
            lim.append(mdim)
            self.r = mdim
        self.limits[-1][-1] = 0
    

class VarDir:
    def __init__(self) -> None:
        self.vardir = dict()

    def add(self, varid: str, vtype: str, addr: int, lims: list = None):
        if varid in self.vardir:
            raise ExistingRow(varid)
        variable = Variable(addr, vtype, lims)
        self.vardir.update({varid:variable})

    def update(self, varid: str, **kwargs):
        var = self.get(varid)
        if var is None:
            raise NonExistentRow(varid)
        for k,v in kwargs.items():
            setattr(var, k, v)
        self.vardir.update({varid:var})

    def get(self, varid) -> Variable:
        return self.vardir.get(varid, None)

    def delete(self, varid):
        if not (varid in self.vardir):
            raise NonExistentRow(varid)
        del self.vardir[varid]

    def get_addr(self) -> list:
        return [v.addr for _,v in self.vardir.items()]

class Function:
    def __init__(self, ftype, glb) -> None:
        self.vtab = VarDir()
        self.auxvtab: list[VarDir] = []
        self.params = VarDir() if (not glb) else None
        self.porder = []
        self.ftype = ftype
        self.returnable = (ftype != Reserved.VOID)
        self.qaddr = None

    @property
    def curr_auxvtab(self):
        if not self.auxvtab:
            return None
        return self.auxvtab[-1]

    def add_auxvtab(self):
        self.auxvtab.append(VarDir())

    def pop_auxvtab(self):
        if not self.auxvtab:
            raise Exception('ParsingError :: Emptying from empty auxvtab stack')
        self.auxvtab.pop()

    def get_var(self, vid):
        for v in self.auxvtab[::-1]:
            if vid in v.vardir:
                return v.get(vid), 0
        if vid in self.vtab.vardir:
            return self.vtab.get(vid), 1
        if self.params:
            if vid in self.params.vardir:
                return self.params.get(vid), 2
        return None, -1

    def dump_addr(self):
        res = []
        for v in self.auxvtab + [self.params, self.vtab]:
            res.append(v.get_addr())
        return res

class FuncDir:
    def __init__(self) -> None:
        self.funcdir = dict()

    def add(self, fid = None, ftype = None, glb = False):
        if fid in self.funcdir:
            raise ExistingRow(fid)
        row = Function(ftype, glb)
        self.funcdir.update({fid:row})

    def get(self, fid) -> Function:
        res = self.funcdir.get(fid, None)
        if res is None:
            raise NonExistentRow(fid)
        return res

    def add_qc(self, fid, qaddr=None):
        row = self.get(fid)
        row.qaddr = qaddr
        self.funcdir.update({fid:row})

class ConstTab:
    def __init__(self) -> None:
        self.data = {
            Reserved.TINT: dict(),
            Reserved.TFLT: dict(),
            Reserved.TBOOL: dict(),
            Reserved.TSTR: dict()
        }

    def __repr__(self) -> str:
        return f'{self.data}'

    def add(self, vtype, value, addr):
        if value in self.data.get(vtype):
            raise ExistingRow(value)
        else:
            self.data[vtype].update({value:addr})

    def get(self, vtype, value):
        return self.data[vtype].get(value, None)
