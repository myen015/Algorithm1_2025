# simple_arithmetic_parser.py

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value      # int or str (operator)
        self.left  = left
        self.right = right

def tokenize(s: str):
    tokens = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1; continue
        if c.isdigit():
            num = 0
            while i < len(s) and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            tokens.append(num)
            continue
        if c in '+-*/()':
            tokens.append(c)
            i += 1
            continue
        raise ValueError(f"Bad char: {c}")
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def consume(self, expected=None):
        tok = self.peek()
        if expected is not None and tok != expected:
            raise SyntaxError(f"Expected {expected}, got {tok}")
        self.i += 1
        return tok

    def parse(self):
        return self.expr()

    def expr(self):            # + and -
        node = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            node = Node(op, node, self.term())
        return node

    def term(self):            # * and /
        node = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            node = Node(op, node, self.factor())
        return node

    def factor(self):          # number or (expr)
        tok = self.peek()
        if isinstance(tok, int):
            self.consume()
            return Node(tok)
        if tok == '(':
            self.consume('(')
            node = self.expr()
            self.consume(')')
            return node
        raise SyntaxError(f"Unexpected {tok}")

def print_tree(node, prefix="", is_last=True):
    print(prefix + ("└── " if is_last else "├── ") + str(node.value))
    children = [c for c in (node.left, node.right) if c]
    for i, child in enumerate(children):
        print_tree(child, prefix + ("    " if is_last else "│   "),
                    i == len(children)-1)

def evaluate(node):
    if isinstance(node.value, int):
        return node.value
    a = evaluate(node.left)
    b = evaluate(node.right)
    return {'+': a+b, '-': a-b, '*': a*b, '/': a/b}[node.value]

# ------------------------------------------------------------
# Correct example with parentheses (exactly the required case)
# ------------------------------------------------------------
if __name__ == "__main__":
    expr = "(12 + 3 - (4 + 6)) / (12 * 2)"
    print("Expression :", expr)

    tree = Parser(tokenize(expr)).parse()

    print("\nExpression tree:")
    print_tree(tree)

    result = evaluate(tree)
    print("\nResult =", result)
