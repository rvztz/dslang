from dslang.util.tokens import Reserved, Symbols, Patterns
from sly import Lexer

class DSLangLexer(Lexer):

    tokens = {
        PROGRAM, FUNCTION, MAIN, VAR, RETURN,          # Palabras del lenguaje
        READ, PRINT, PLOT,

        TINT, TFLT, TSTR, DFRAME, TBOOL, TRUE, FALSE,    # Tipos
        VOID,    

        IF, ELSE, FOR, TO, WHILE, DO,                   # Condicional y ciclos

        AND, OR, EQ, NOTEQ, GT, LT,             # Operadores booleanos
        LTEQ, GTEQ,

        SHRT, ASGN, ADD, SUB, MULT, DIV, EXP,                 # Operadores

        ID, CTEFLT, CTEINT, CTESTR,                     # Identificador y constantes

        COMMA, SCOLON, COLON, LCURL, RCURL,             # Literales
        LPAREN, RPAREN, LBRCKT, RBRCKT
    }
    ignore = ' \t'

    # TOKEN DEFINITION
    COMMA   = Symbols.COMMA
    SCOLON  = Symbols.SCOLON
    COLON   = Symbols.COLON
    LCURL   = Symbols.LCURL
    RCURL   = Symbols.RCURL
    LPAREN  = Symbols.LPAREN
    RPAREN  = Symbols.RPAREN
    LBRCKT  = Symbols.LBRCKT
    RBRCKT  = Symbols.RBRCKT

    ADD     = Symbols.ADD
    SUB     = Symbols.SUB
    EXP     = Symbols.EXP
    MULT    = Symbols.MULT
    DIV     = Symbols.DIV

    EQ      = Symbols.EQ
    SHRT    = Symbols.SHRT
    ASGN    = Symbols.ASGN
    GTEQ   = Symbols.GTEQ
    GT  = Symbols.GT
    LTEQ   = Symbols.LTEQ
    LT  = Symbols.LT
    NOTEQ   = Symbols.NOTEQ
    AND     = Symbols.AND
    OR      = Symbols.OR

    CTEFLT  = Patterns.CTEFLT
    CTEINT  = Patterns.CTEINT
    CTESTR  = Patterns.CTESTR
    TRUE    = Reserved.TRUE
    FALSE   = Reserved.FALSE

    ID = Patterns.ID
    ID[Reserved.PROGRAM]     = PROGRAM
    ID[Reserved.FUNCTION]    = FUNCTION
    ID[Reserved.MAIN]        = MAIN
    ID[Reserved.VAR]         = VAR
    ID[Reserved.RETURN]      = RETURN
    ID[Reserved.READ]        = READ
    ID[Reserved.PRINT]       = PRINT
    ID[Reserved.PLOT]        = PLOT

    ID[Reserved.TFLT]       = TFLT
    ID[Reserved.TINT]       = TINT
    ID[Reserved.TSTR]       = TSTR
    ID[Reserved.TBOOL]      = TBOOL
    ID[Reserved.DFRAME]     = DFRAME
    ID[Reserved.VOID]       = VOID

    # HELPER FUNCTIONS
    def CTEFLT(self, t):
        t.value = float(t.value)
        return t
    
    def CTEINT(self, t):
        t.value = int(t.value)
        return t
    
    def CTESTR(self, t):
        t.value = str(t.value)
        return t

    def TRUE(self, t):
        t.value = bool(t.value)
        return t

    def FALSE(self, t):
        t.value = bool(t.value)
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    





    

    

    

