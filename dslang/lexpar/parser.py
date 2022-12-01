from sly import Parser
import logging
from dslang.lexpar.lexer import DSLangLexer
from dslang.lexpar.ctx import ParsingCtx, ParsingScope
from dslang.util.tokens import Reserved, Symbols, ExecTok
class DSLangParser(Parser):

    start = 'program'
    tokens = DSLangLexer.tokens
    ctx = ParsingCtx()
    ptype_to_token = dict(int=Reserved.TINT, float = Reserved.TFLT, 
                        str = Reserved.TSTR, bool= Reserved.TBOOL)
    #debugfile = 'dslang.out'
    log = logging.getLogger(__name__)
    log.setLevel(logging.CRITICAL)

    precedence = (
       ('left', ADD, SUB),
       ('left', MULT, DIV))

    @_('PROGRAM ID add_pid SCOLON progitem')
    def program(self, p):
        return p

    @_('statement programdv',
        'vars programdv',
        'function programdv',
        'main programdv')
    def progitem(self, p):
        return p

    @_('progitem', 'empty')
    def programdv(self, p):
        return p[-1]

    @_('MAIN LPAREN RPAREN LCURL maindv')
    def main(self, p):
        return p

    @_('vars maindv',
        'statement maindv')
    def maindv(self, p):
        return p[0],p[1]
    
    @_('RCURL')
    def maindv(self, p):
        return p[0]

    @_('VAR vtype add_cvtype COLON listids SCOLON reset_vtype')
    def vars(self, p):
        return p
    
    @_('TBOOL','TINT',
        'TFLT', 'TSTR')
    def vtype(self, p):
        return p[0]
    
    @_('ID store_varid listdv')
    def listids(self, p):
        return p
    
    @_('ID LBRCKT CTEINT RBRCKT store_arrid dimlist def_dims listdv')
    def listids(self, p):
        pass

    @_('LBRCKT CTEINT RBRCKT append_dim dimlist')
    def dimlist(self, p):
        return p
    
    @_('empty')
    def dimlist(self, p):
        pass
    
    @_('COMMA listids')
    def listdv(self, p):
        return p[1]
    
    @_('empty')
    def listdv(self, p):
        return p[0]

    @_('FUNCTION typefunc ID save_func LPAREN funcparams RPAREN LCURL add_fqid funcstat remove_fscope')
    def function(self, p):
        return p

    @_('vtype','VOID')
    def typefunc(self, p):
        return p[0]
    
    @_('params','empty')
    def funcparams(self, p):
        return p[0]

    @_('vtype ID save_param paramsdv')
    def params(self, p):
        return p[-1]

    @_('COMMA params')
    def paramsdv(self, p):
        return p

    @_('empty')
    def paramsdv(self, p):
        return p
    
    @_('vars funcstat', 
        'statement funcstat')
    def funcstat(self, p):
        return p
    
    @_('RCURL')
    def funcstat(self, p):
        return p[0]

    @_('expr', 'assign SCOLON', 'shrtassgn SCOLON','funccall SCOLON', 'read SCOLON', 'pprint SCOLON', 'cond',
        'wwhile', 'rreturn SCOLON')
    def statement(self, p):
        pass

    @_('exprdv')
    def expr(self, p):
        expres = p[0]
        self.ctx.egen.operand_ctx[-1].pop()
        return expres

    @_('bexp AND add_oper exprdv check_expr_st',
        'bexp OR add_oper exprdv check_expr_st')
    def exprdv(self, p):
        return self.ctx.egen.operand_ctx[-1][-1]
    
    @_('bexp check_expr_st')
    def exprdv(self, p):
        return self.ctx.egen.operand_ctx[-1][-1]

    @_('asexp LT add_oper bexp check_bexp_st',
        'asexp GT add_oper bexp check_bexp_st',
        'asexp EQ add_oper bexp check_bexp_st',
        'asexp NOTEQ add_oper bexp check_bexp_st',
        'asexp LTEQ add_oper bexp check_bexp_st',
        'asexp GTEQ add_oper bexp check_bexp_st')
    def bexp(self, p):
        return p
    
    @_('asexp check_bexp_st')
    def bexp(self, p):
        return p

    @_('emdexp ADD add_oper asexp check_asexp_st',
        'emdexp SUB add_oper asexp check_asexp_st')
    def asexp(self, p):
        return p

    @_('emdexp check_asexp_st')
    def asexp(self, p):
        return p

    @_('pexp EXP add_oper emdexp check_emdexp_st',
        'pexp MULT add_oper emdexp check_emdexp_st',
        'pexp DIV add_oper emdexp check_emdexp_st')
    def emdexp(self, p):
        return p

    @_('pexp check_emdexp_st')
    def emdexp(self, p):
        return p
    
    @_('LPAREN push_oper_ctx exprdv RPAREN pop_oper_ctx')
    def pexp(self, p):
        return p
    
    @_('const save_const',
        'ID add_vid',
        'varidx add_vidx',
        'funccall add_funcv')
    def pexp(self, p):
        return p

    @_('ID ASGN expr gen_assign')
    def assign(self, p):
        return p

    @_('varidx add_vidx ASGN expr gen_idx_assign')
    def assign(self, p):
        return p

    @_('ID SHRT expr gen_shrt_assign')
    def shrtassgn(self, p):
        return p

    @_('ID FCALL LPAREN validate_fid fcallparams RPAREN add_curr_pquad')
    def funccall(self, p):
        return p[0]

    @_('fcallterm fcallparamdv', 'empty')
    def fcallparams(self, p):
        return p[0]

    @_('COMMA fcallparams', 'empty')
    def fcallparamdv(self, p):
        pass

    @_('ID ASGN expr add_params')
    def fcallterm(self, p):
        return p[0]

    @_('READ LPAREN ID RPAREN gen_read', 
        'READ LPAREN varidx add_vidx gen_idxread RPAREN')
    def read(self, p):
        return p
    
    @_('PRINT LPAREN printlist RPAREN gen_print_quads')
    def pprint(self, p):
        return p

    @_('printerm printlistdv')
    def printlist(self, p):
        pass

    @_('COMMA printerm')
    def printlistdv(self, p):
        pass

    @_('empty')
    def printlistdv(self, p):
        pass

    @_('ID push_printid',
        'varidx add_vidx push_printidl',
        'CTESTR push_printct')
    def printerm(self, p):
        return p

    @_('IF LPAREN expr RPAREN LCURL gen_cond_quad condst RCURL add_jquad')
    def cond(self, p):
        return p

    @_('IF LPAREN expr RPAREN LCURL gen_cond_quad condst RCURL gen_egoto ELSE LCURL condst RCURL add_jquad')
    def cond(self, p):
        return p

    @_('statement condstdv')
    def condst(self, p):
        return p

    @_('condst')
    def condstdv(self, p):
        return p 

    @_('empty')
    def condstdv(self, p):
        return p

    @_('WHILE add_wpquad LPAREN expr RPAREN gen_wquad DO LCURL whiledv add_wquad')
    def wwhile(self, p):
        return p

    @_('statement whiledv')
    def whiledv(self, p):
        return p

    @_('RCURL')
    def whiledv(self, p):
        return p

    # @_('FOR ID ASGN CTEINT TO expr LBRCKT fordv')
    # def ffor(self, p):
    #     return p

    # @_('statement fordv')
    # def fordv(self, p):
    #     return p

    # @_('RBRCKT')
    # def fordv(self, p):
    #     return p

    @_('RETURN expr check_return')
    def rreturn(self, p):
        return p

    @_('TRUE', 'FALSE', 'CTEFLT',
        'CTEINT', 'CTESTR')
    def const(self, p):
        return p[-1]
        
    @_('ID LBRCKT validate_arr expr RBRCKT gen_vdim arrindex')
    def varidx(self, p):
        return p[0]

    @_('LBRCKT expr RBRCKT gen_vdim arrindex')
    def arrindex(self, p):
        pass

    @_('empty')
    def arrindex(self, p):
        pass

    # NOTE:Producción vacía
    @_('')
    def empty(self, p):
        pass
    
    # NOTE: Definición de puntos neurálgicos
    @_('')
    def add_pid(self, p):
        if (pid := self.ctx.p_id):
            raise SystemExit(f'DSLang error => Existing pid: {pid}.')
        self.ctx.funcdir.add(f'___pid_{p[-1]}', Reserved.VOID, True)
        self.ctx.add_fctx(f'___pid_{p[-1]}')
        self.ctx.p_id = self.ctx.curr_fctx
        self.ctx.set_pscope(ParsingScope.GLOBAL)

    @_('')
    def add_cvtype(self, p):
        self.ctx.curr_vtype = p[-1]

    @_('')
    def reset_vtype(self, p):
        self.ctx.curr_vtype = ''

    @_('')
    def store_varid(self, p):
        try:
            addr = self.ctx.mem.alloc(self.ctx.curr_pscope, self.ctx.curr_vtype)
            self.ctx.add_var(p[-1], self.ctx.curr_vtype, addr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def store_arrid(self, p):
        try:
            self.ctx.curr_vid = p[-4]
            self.ctx.add_var(self.ctx.curr_vid, self.ctx.curr_vtype, -1, [0, p[-2]])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)
    
    @_('')
    def append_dim(self, p):
        try:
            var = self.ctx.get_var(self.ctx.curr_vid)
            var.add_dim([0, p[-2]])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def def_dims(self, p):
        try:
            var = self.ctx.get_var(self.ctx.curr_vid)
            var.set_mdim()
            addr = self.ctx.mem.alloc(self.ctx.curr_pscope, self.ctx.curr_vtype, var.size)
            self.ctx.update_var(self.ctx.curr_vid, addr = addr)
            self.ctx.curr_vid = ''
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def save_const(self, p):
        val = p[-1]
        const_type = self.ptype_to_token.get(type(val).__name__, None)
        if not const_type:
            raise SystemExit('DSLang error => Unsupported const type')
        if const_addr := self.ctx.consts.get(const_type, val):
            self.ctx.egen.add_operand(const_addr, const_type)
            return const_addr, const_type
        else:
            addr = self.ctx.mem.alloc('const', const_type)
            self.ctx.mem.set_memval(addr, val)
            self.ctx.consts.add(const_type, val, addr)
            self.ctx.egen.add_operand(addr, const_type)
            return addr, const_type

    @_('')
    def add_vid(self, p):
        try:
            var = self.ctx.get_var(p[-1])
            self.ctx.egen.add_operand(var.addr, var.vtype)
            return var.addr, var.vtype
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def validate_arr(self, p):
        try:
            self.ctx.curr_vid = p[-2]
            var = self.ctx.get_var(self.ctx.curr_vid)
            if not (var.is_array):
                raise Exception('IndexError :: Indexing for non-array variable')
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def gen_vdim(self, p):
        try:
            exp_res = p[-2]
            if exp_res['ptype'] != Reserved.TINT:
                raise Exception(f'IndexError :: Invalid type for indexing')
            var = self.ctx.get_var(self.ctx.curr_vid)
            if self.ctx.curr_dim > len(var.limits):
                raise Exception(f'IndexError :: Invalid indexing for {len(var.limits)}-dimension')
            limits = var.limits[self.ctx.curr_dim-1]
            self.ctx.add_quad(ExecTok.VERIF, exp_res['pid'], 
                                            0, limits[1])
            if self.ctx.curr_dim == len(var.limits):
                self.ctx.curr_dim += 1
                self.ctx.idx_agg.append(exp_res['pid'])
            else:
                taddr = self.ctx.mem.alloc('temporal', Reserved.TINT)
                self.ctx.add_quad(Symbols.C_MULT, exp_res['pid'], limits[2], taddr, None, literal = ['r'])
                self.ctx.curr_dim += 1
                self.ctx.idx_agg.append(taddr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_vidx(self, p):
        try:
            while len(self.ctx.idx_agg) > 1:
                l,r = self.ctx.idx_agg.popleft(), self.ctx.idx_agg.popleft()
                taddr = self.ctx.mem.alloc('temporal', Reserved.TINT)
                self.ctx.idx_agg.appendleft(taddr)
                self.ctx.add_quad(Symbols.C_ADD, l, r, taddr)
            ref = self.ctx.idx_agg.pop()
            var = self.ctx.get_var(self.ctx.curr_vid)
            taddr = self.ctx.mem.alloc('temporal', Reserved.TINT)
            self.ctx.add_quad(Symbols.C_ADD, ref, var.addr, taddr, None, literal = ['r'])
            self.ctx.egen.add_operand(taddr,var.vtype,True)
            self.ctx.curr_dim = 1
            self.ctx.curr_vid = ''
            return ref, ExecTok.REFERENCE
        except Exception as e:
            raise SystemExit('DSLang error => ', e)
            
    @_('')
    def add_oper(self, p):
        self.ctx.egen.curr_operator_st.append(p[-1])
    
    @_('')
    def check_expr_st(self, p):
        curr_operator = self.ctx.toperator
        if curr_operator and (curr_operator in {Symbols.AND, Symbols.C_OR}):
            self.ctx.gen_expr()

    @_('')
    def check_bexp_st(self, p):
        curr_operator = self.ctx.toperator
        if curr_operator and (curr_operator in {Symbols.LT, Symbols.GT, Symbols.EQ, Symbols.NOTEQ, Symbols.LTEQ, Symbols.GTEQ}):
            self.ctx.gen_expr()

    @_('')
    def check_asexp_st(self, p):
        curr_operator = self.ctx.toperator
        if curr_operator and (curr_operator in {Symbols.C_ADD, Symbols.SUB}):
            self.ctx.gen_expr()

    @_('')
    def check_emdexp_st(self, p):
        curr_operator = self.ctx.toperator
        if curr_operator and (curr_operator in {Symbols.C_EXP, Symbols.C_MULT, Symbols.DIV}):
            self.ctx.gen_expr()

    @_('')
    def push_oper_ctx(self, p):
        self.ctx.egen.create_operand_ctx()

    @_('')
    def pop_oper_ctx(self, p):
        self.ctx.egen.pop_operand_ctx()

    @_('')
    def gen_assign(self, p):
        try:
            exp_res = p[-1]
            var = self.ctx.get_var(p[-3])
            self.ctx.add_quad(Symbols.ASGN, None, exp_res['pid'], var.addr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def gen_idx_assign(self, p):
        try:
            idx = self.ctx.egen.curr_operand_st.pop()
            exp_res = p[-1]
            self.ctx.add_quad(Symbols.ASGN, None, exp_res['pid'], idx['pid'], deref=['v'])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def gen_shrt_assign(self, p):
        try:
            varid = p[-3]
            exp_res = p[-1]
            addr = self.ctx.mem.alloc(self.ctx.curr_pscope, exp_res['ptype'])
            self.ctx.add_var(varid, exp_res['ptype'], addr)
            self.ctx.add_quad(Symbols.ASGN, None, exp_res['pid'], addr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def gen_read(self, p):
        try:
            var = self.ctx.get_var(p[-2])
            self.ctx.add_quad(p[-4], None, None, var.addr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)


    @_('')
    def gen_idxread(self, p):
        try:
            idx = self.ctx.egen.curr_operand_st.pop()
            self.ctx.add_quad(p[-4], None, None, idx['pid'], deref=['v'])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def push_printid(self, p):
        try:
            var = self.ctx.get_var(p[-1])
            self.ctx.print_items.append([var.addr, False])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def push_printidl(self, p):
        try:
            idx = self.ctx.egen.curr_operand_st.pop()
            self.ctx.print_items.append([idx['pid'], True])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def push_printct(self, p):
        try:
            const = p[-1]
            const_type = self.ptype_to_token.get(type(const).__name__, None)
            if const_addr := self.ctx.consts.get(const_type, const):
                self.ctx.print_items.append([const_addr, False])
            else:
                addr = self.ctx.mem.alloc('const', const_type)
                self.ctx.mem.set_memval(addr, const)
                self.ctx.consts.add(const_type, const, addr)
                self.ctx.print_items.append([addr, False])
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def gen_print_quads(self, p):
        self.ctx.gen_print_quads()

    @_('')
    def gen_cond_quad(self, p):
        try:
            exp_res = p[-3]
            if exp_res['ptype'] != Reserved.TBOOL:
                raise Exception(f'TypeError :: Conditional expression should be of type: {Reserved.TBOOL}')
            self.ctx.add_quad(ExecTok.GOTOF, None, exp_res['pid'], None)
            self.ctx.add_pquad(self.ctx.curr_qidx-1)
            self.ctx.set_pscope(ParsingScope.LOCAL)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_jquad(self, p):
        goto_idx = self.ctx.pop_pquad()
        self.ctx.update_quad(goto_idx, v=self.ctx.curr_qidx)
        self.ctx.reset_pscope()

    @_('')
    def gen_egoto(self, p):
        goto_idx = self.ctx.pop_pquad()
        self.ctx.add_quad(ExecTok.GOTO, None, None, None)
        self.ctx.update_quad(goto_idx, v=self.ctx.curr_qidx)
        self.ctx.add_pquad(self.ctx.curr_qidx-1)
        self.ctx.reset_pscope()
        self.ctx.set_pscope(ParsingScope.LOCAL)

    @_('')
    def add_wpquad(self, p):
        self.ctx.add_pquad(self.ctx.curr_qidx)

    @_('')
    def gen_wquad(self, p):
        try:
            exp_res = p[-2]
            if exp_res['ptype'] != Reserved.TBOOL:
                raise Exception(f'TypeError :: Loop expression should be of type: {Reserved.TBOOL}')
            self.ctx.add_quad(ExecTok.GOTOF, None, exp_res['pid'], None)
            self.ctx.add_pquad(self.ctx.curr_qidx-1)
            self.ctx.set_pscope(ParsingScope.LOCAL)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_wquad(self, p):
        idx_gotof = self.ctx.pop_pquad()
        idx_goto = self.ctx.pop_pquad()
        self.ctx.add_quad(ExecTok.GOTO, None, None, idx_goto)
        self.ctx.update_quad(idx_gotof, v=self.ctx.curr_qidx)
        self.ctx.reset_pscope()

    @_('') 
    def save_func(self, p):
        try:
            ftype = p[-2]
            funcid = ExecTok.RETFUNC + p[-1]
            if ftype != Reserved.VOID:
                addr = self.ctx.mem.alloc(self.ctx.curr_pscope, ftype)
                self.ctx.p_func.vtab.add(funcid, ftype, addr)
            self.ctx.add_pquad(self.ctx.curr_qidx)
            self.ctx.add_quad(ExecTok.BFUNC, None, None, None)
            self.ctx.funcdir.add(funcid, ftype, False)
            self.ctx.add_fctx(funcid)
            self.ctx.set_pscope(ParsingScope.FUNCTION)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def save_param(self, p):
        try:
            if self.ctx.curr_fctx == self.ctx.p_id:
                raise Exception('SyntaxError :: Param definition outside of function')
            varid = p[-1]
            vtype = p[-2]
            addr = self.ctx.mem.alloc('function', vtype)
            self.ctx.curr_func.params.add(varid,vtype, addr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_fqid(self, p):
        self.ctx.funcdir.add_qc(self.ctx.curr_fctx, qaddr = self.ctx.curr_qidx+1)

    @_('')
    def check_return(self, p):
        exp_res = p[-1]
        fvar = self.ctx.p_func.vtab.get(self.ctx.curr_fctx)
        if fvar.vtype != exp_res['ptype']:
            raise Exception('TypeError :: Expression return should match function value')
        self.ctx.add_quad(Symbols.ASGN, None, exp_res['pid'], fvar.addr)

    @_('')
    def remove_fscope(self, p):
        self.ctx.reset_pscope()
        self.ctx.pop_fctx()
        idx_bfunc = self.ctx.pop_pquad()
        self.ctx.add_quad(ExecTok.ENDFUNC, None, None, None)
        self.ctx.update_quad(idx_bfunc, v=self.ctx.curr_qidx-1)
        #self.ctx.clean_function_mem()


    @_('')
    def validate_fid(self, p):
        try:
            fid = ExecTok.RETFUNC + p[-3]
            func = self.ctx.funcdir.get(fid)
            self.ctx.curr_fid = fid
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_funcv(self, p):
        try:
            fid = ExecTok.RETFUNC + p[-1]
            fvar = self.ctx.p_func.vtab.get(fid)
            if fvar.vtype == Reserved.VOID:
                raise Exception('TypeError :: Non-returnable function called as term')
            self.ctx.egen.add_operand(fvar.addr, fvar.vtype)
            return fvar.addr, fvar.vtype
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_params(self, p):
        try:
            param = self.ctx.funcdir.get(self.ctx.curr_fid).params.get(p[-3])
            if not param:
                raise Exception('SyntaxError :: invalid function parma')
            exp_res = p[-1]
            self.ctx.add_quad(ExecTok.PARAM, None, exp_res['pid'], param.addr)
        except Exception as e:
            raise SystemExit('DSLang error => ', e)

    @_('')
    def add_curr_pquad(self, p):
        fvar = self.ctx.funcdir.get(self.ctx.curr_fid)
        self.ctx.add_quad(ExecTok.GOSUB, None, fvar.qaddr, self.ctx.curr_qidx+2)
        self.ctx.curr_fid = ''
