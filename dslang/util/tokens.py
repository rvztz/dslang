""" Constantes usadas por el la clase de lexing"""
class Reserved:
    PROGRAM =  "program"
    FUNCTION = "func"
    MAIN =     "main"
    VAR =     "var"
    RETURN =   "return"
    TINT =     "int"
    TFLT =     "float"
    TSTR =     "string"
    DFRAME =   "df"
    TBOOL =    "bool" 
    TRUE =     "True"
    FALSE =    "False"
    VOID =     "void"
    READ =     "read"
    PRINT =    "write"
    IF =       "if"
    THEN =     "then"
    ELSE =     "else"
    FOR =      "for",
    TO =       "to",
    WHILE =    "while",
    DO =       "do",
    PLOT =     "plot"


class Symbols:
    COMMA =    r","
    SCOLON =   r";"
    COLON =    r":"
    LCURL =    r"{"
    RCURL =    r"}"
    LPAREN =   r"\("
    RPAREN =   r"\)"
    LBRCKT =   r"\["
    RBRCKT =   r"\]"
    LT =       r"<"
    GT =       r">"
    LTEQ =     r"<="
    GTEQ =     r">="
    NOTEQ =    r"!="
    EQ =       r"=="
    AND =      r"&&"
    OR =       r"\|\|"
    ASGN =     r"="
    SHRT =     r":="
    ADD =      r"\+"
    SUB =      r"-"
    MULT =     r"\*"
    DIV =      r"/"
    EXP =      r"\*\*"

    # Símbolos sin regex-formatting   
    C_LPAREN =   r"("
    C_RPAREN =   r")"
    C_LBRCKT =   r"["
    C_RBRCKT =   r"]"
    C_OR     =   r"||"
    C_ADD    =   r"+"
    C_MULT   =   r"*"
    C_EXP    =   r"**"


class Patterns:
    ID =      r"[a-zA-Z_][a-zA-Z0-9_]*"
    CTEFLT =  r"\d+\.\d+"
    CTEINT =  r"\d+"
    CTESTR =  r"\'(.*)\'"
    CTECHR =  r"\'(.)\'{1}"

class ExecTok:
    GOTO = 'goto'
    GOTOF = 'gotof'
    GOTOV = 'gotov'
    GOSUB = 'gosub'
    PARAM = 'param'
    VERIF = 'verif'
    ENDFUNC = 'endfunc'
    REFERENCE = 'reference'
    RETFUNC = '___f_ret_'
