from dslang.util.tokens import Symbols


class QuadsInstructions:
    def goto(self, q):
        pass

    def gotof(self, q):
        pass

    def gotov(self, q):
        pass

    def gosub(self, q):
        pass

    def verif(self, q):
        pass


class QuadExecutor:
    
    operations = {
        Symbols.AND: lambda x,y: x and y,
        Symbols.C_OR: lambda x,y: x or y,
        Symbols.LT: lambda x,y: x < y,
        Symbols.GT: lambda x,y: x > y,
        Symbols.LTEQ: lambda x,y: x <= y,
        Symbols.GTEQ: lambda x,y: x >= y,
        Symbols.C_ADD: lambda x,y: x + y,
        Symbols.SUB: lambda x,y: x - y,
        Symbols.C_EXP: lambda x,y: x ** y,
        Symbols.C_MULT: lambda x,y: x * y,
        Symbols.DIV: lambda x,y: x / y,
    }

    def __init__(self, quads) -> None:
        self.quads = quads