from dslang.lexpar.lexer import DSLangLexer
from dslang.lexpar.parser import DSLangParser

lexer = DSLangLexer()
parser = DSLangParser()

while True:
    try:
        raw = input('>')
        toks = lexer.tokenize(raw)
        res = parser.parse(toks)
        print('end_parse quads', parser.ctx.quads)
        print('end_parse curr_operand', parser.ctx.egen.curr_operand_st)
        print('end_parse curr_operator', parser.ctx.egen.curr_operator_st)
    except EOFError:
        break


    
