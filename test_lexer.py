from dslang.lexpar.lexer import DSLangLexer

lexer = DSLangLexer()
while True:
    s = input('>')
    for tok in lexer.tokenize(s):
        print('=> ', tok)
