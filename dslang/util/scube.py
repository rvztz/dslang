from dslang.util.types import CAYER_ASSOC

class SemanticCube:

    def __init__(self):
        self.data = CAYER_ASSOC

    def __repr__(self) -> str:
        return f'{self.data}'

    def get(self, tlop, trop, oper):
        return self.data.get(tlop).get(trop).get(oper)
