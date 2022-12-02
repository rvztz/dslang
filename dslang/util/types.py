from dslang.util.tokens import Reserved, Symbols

## NOTE: Definición de tipos
INT     = Reserved.TINT
BOOL    = Reserved.TBOOL
FLOAT   = Reserved.TFLT
STRING  = Reserved.TSTR
ERROR   = None

## NOTE: Asociación para INT
INT_INT_ASSOC = {
    Symbols.C_EXP:  INT,
    Symbols.DIV:  INT,
    Symbols.C_MULT: INT,
    Symbols.C_ADD:  INT,
    Symbols.SUB:  INT,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       BOOL, 
    Symbols.NOTEQ:    BOOL,
    Symbols.GTEQ:    BOOL,
    Symbols.GT:   BOOL,
    Symbols.LTEQ:    BOOL,
    Symbols.LT:   BOOL,
}

INT_FLOAT_ASSOC = {
    Symbols.C_EXP:  FLOAT,
    Symbols.DIV:  FLOAT,
    Symbols.C_MULT: FLOAT,
    Symbols.C_ADD:  FLOAT,
    Symbols.SUB:  FLOAT,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       BOOL, 
    Symbols.NOTEQ:    BOOL,
    Symbols.GTEQ:    BOOL,
    Symbols.GT:   BOOL,
    Symbols.LTEQ:    BOOL,
    Symbols.LT:   BOOL,

    Symbols.EQ:     INT
}

INT_BOOL_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR

}

INT_STR_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR

}

INT_ASSOC = {INT:INT_INT_ASSOC, FLOAT:INT_FLOAT_ASSOC, 
            BOOL: INT_BOOL_ASSOC, STRING: INT_STR_ASSOC}



## NOTE: Asociación para FLOAT
FLOAT_FLOAT_ASSOC = {
    Symbols.C_EXP:  FLOAT,
    Symbols.DIV:  FLOAT,
    Symbols.C_MULT: FLOAT,
    Symbols.C_ADD:  FLOAT,
    Symbols.SUB:  FLOAT,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       BOOL, 
    Symbols.NOTEQ:    BOOL,
    Symbols.GTEQ:    BOOL,
    Symbols.GT:   BOOL,
    Symbols.LTEQ:    BOOL,
    Symbols.LT:   BOOL,

    Symbols.EQ:     FLOAT
}

FLOAT_INT_ASSOC = {
    Symbols.C_EXP:  FLOAT,
    Symbols.DIV:  FLOAT,
    Symbols.C_MULT: FLOAT,
    Symbols.C_ADD:  FLOAT,
    Symbols.SUB:  FLOAT,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       BOOL, 
    Symbols.NOTEQ:    BOOL,
    Symbols.GTEQ:    BOOL,
    Symbols.GT:   BOOL,
    Symbols.LTEQ:    BOOL,
    Symbols.LT:   BOOL,

    Symbols.EQ:     FLOAT
}

FLOAT_BOOL_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR

}

FLOAT_STR_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR

}

FLOAT_ASSOC = {INT:FLOAT_INT_ASSOC, FLOAT:FLOAT_FLOAT_ASSOC, 
            BOOL:FLOAT_BOOL_ASSOC, STRING:FLOAT_STR_ASSOC}

## NOTE: Asociación para STR

STR_STR_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  STRING,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       BOOL, 
    Symbols.NOTEQ:    BOOL,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     STRING
}

STR_INT_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR
}

STR_FLOAT_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR
}

STR_BOOL_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR
}

STR_ASSOC = {INT:STR_INT_ASSOC, FLOAT:STR_FLOAT_ASSOC, 
            BOOL:STR_BOOL_ASSOC, STRING:STR_STR_ASSOC}


## NOTE: Asociación para BOOL

BOOL_BOOL_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   BOOL,
    Symbols.AND:  BOOL,

    Symbols.EQ:       BOOL, 
    Symbols.NOTEQ:    BOOL,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     BOOL
}

BOOL_INT_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR
}

BOOL_FLOAT_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR
}

BOOL_STR_ASSOC = {
    Symbols.C_EXP:  ERROR,
    Symbols.DIV:  ERROR,
    Symbols.C_MULT: ERROR,
    Symbols.C_ADD:  ERROR,
    Symbols.SUB:  ERROR,
    
    Symbols.C_OR:   ERROR,
    Symbols.AND:  ERROR,

    Symbols.EQ:       ERROR, 
    Symbols.NOTEQ:    ERROR,
    Symbols.GTEQ:    ERROR,
    Symbols.GT:   ERROR,
    Symbols.LTEQ:    ERROR,
    Symbols.LT:   ERROR,

    Symbols.EQ:     ERROR
}

BOOL_ASSOC = {INT:BOOL_INT_ASSOC, FLOAT:BOOL_FLOAT_ASSOC, 
            BOOL:BOOL_BOOL_ASSOC, STRING:BOOL_STR_ASSOC}


# NOTE: Cubo semántico
CAYER_ASSOC = {
    INT: INT_ASSOC,
    FLOAT: FLOAT_ASSOC,
    BOOL: BOOL_ASSOC,
    STRING: STR_ASSOC
} 

