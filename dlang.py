import sys
import pprint
from dslang.lexpar.lexer import DSLangLexer
from dslang.lexpar.parser import DSLangParser
from dslang.vm.exec import QuadExecutor


def format_qidx(i):
    return f'{i}{"".join([" " for x in range(6-len(str(i)))])}::'

def tokenize(st, debug):
    lexer = DSLangLexer()
    parser = DSLangParser()

    toks = lexer.tokenize(st)
    _ = parser.parse(toks)
    if debug:
        print('----------- quads: \n')
        for i in range(len(parser.ctx.quads)): print(format_qidx(i), parser.ctx.quads[i])
        print('----------- vtab: \n')
        pprint.pprint(parser.ctx.curr_func.vtab.vardir)
        print('----------- curr_operand: \n')
        pprint.pprint(parser.ctx.egen.curr_operand_st)
        print('----------- curr_operator: \n')
        pprint.pprint(parser.ctx.egen.curr_operator_st)
        print('-----------')
        print('Starting exec ...')
    ex = QuadExecutor(parser.ctx.mem, parser.ctx.quads, debug)
    ex.exec_quads()

if __name__ == '__main__':
    filepath = sys.argv[1]
    dbg = False
    if len(sys.argv) > 2:
        dbg = (sys.argv[2] == '--debug')
    global debug
    debug = dbg
    f = open(filepath, 'r')
    f = ''.join(f.read())
    tokenize(f, debug)