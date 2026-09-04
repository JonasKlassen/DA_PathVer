class Node:
    pass


# -------- Expressions --------

class AstInt(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Int({self.value})"

class AstBool(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Bool({self.value})"

class Var(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"


class ArrayAccess(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return f"{self.name}[{self.index}]"


# -------- Statements --------

class RefArg(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Ref({self.name})"


class Arg(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Assign(Node):
    def __init__(self, target, value, index=None):
        self.target = target
        self.value = value
        self.index = index

    def __repr__(self):
        return f"{self.index}: Assign({self.target}, {self.value})"


class Call(Node):
    def __init__(self, expr, args, index=None):
        self.expr = expr
        self.args = args
        self.index = index

    def __repr__(self):
        return f"{self.index}: Call({self.expr}, {self.args})"


class Return(Node):
    def __init__(self, expr, index=None):
        self.expr = expr
        self.index = index

    def __repr__(self):
        return f"{self.index}: Return({self.expr})"


class Repeat(Node):
    def __init__(self, index=None):
        self.index = index

    def __repr__(self):
        return f"{self.index}: Repeat"


class Function(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Function({self.name}, params={self.params}, body={self.body})"


class Program(Node):
    def __init__(self, local_vars, global_vars, functions):
        self.local_vars = local_vars
        self.global_vars = global_vars
        self.functions = functions

    def __repr__(self):
        return f"Program(local={self.local_vars}, global={self.global_vars}, functions={self.functions})"
