class Node:
    pass


class Init(Node):
    def __init__(self, formula):
        self.formula = formula

    def __repr__(self):
        return f"Init({self.formula})"


class AstInt(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Int({self.value})"

class Var(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        if self.index is not None:
            return f"Var({self.name}[{self.index}])"
        return f"Var({self.name})"

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"


class UnOp(Node):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __repr__(self):
        return f"UnOp({self.op}, {self.value})"


class Modal(Node):
    def __init__(self, mode, trace, formula):
        self.mode = mode
        self.trace = trace
        self.formula = formula

    def __repr__(self):
        return f"Modal({self.mode}, {self.trace}, {self.formula})"


class AtFn(Node):
    def __repr__(self):
        return "AtFn()"


class Quantifier(Node):
    def __init__(self, qtype, var, formula):
        self.qtype = qtype
        self.var = var
        self.formula = formula

    def __repr__(self):
        return f"Quantifier({self.qtype}, {self.var}, {self.formula})"


class TraceAtom(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"TraceAtom({self.value})"
