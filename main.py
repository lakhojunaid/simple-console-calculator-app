#Token types
NUMBER = "NUMBER"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
EOF = "EOF"

# Token class
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}({self.value})"
        return f"{self.type}"

# AST Nodes
class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class BinOpNode:
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token  # PLUS, MINUS, MUL, DIV
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op_token}, {self.right})"

    

# Tokenizer / Lexer
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char == " ":
            self.advance()

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char == " ":
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                tokens.append(Token(NUMBER, self.number()))
                continue

            if self.current_char == "+":
                tokens.append(Token(PLUS, "+"))
                self.advance()
                continue

            if self.current_char == "-":
                tokens.append(Token(MINUS, "-"))
                self.advance()
                continue

            if self.current_char == "*":
                tokens.append(Token(MUL, "*"))
                self.advance()
                continue

            if self.current_char == "/":
                tokens.append(Token(DIV, "/"))
                self.advance()
                continue

            if self.current_char == "(":
                tokens.append(Token(LPAREN, "("))
                self.advance()
                continue

            if self.current_char == ")":
                tokens.append(Token(RPAREN, ")"))
                self.advance()
                continue

            raise Exception(f"Invalid character: {self.current_char}")

        tokens.append(Token(EOF))
        return tokens
    
# Parser (Recursive Descent)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(EOF)

    def parse(self):
        node = self.expr()
        if self.current_token.type != EOF:
            raise Exception("Unexpected token after expression")
        return node

    # expr -> term ((PLUS | MINUS) term)*
    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op_token = self.current_token
            self.advance()
            right = self.term()
            node = BinOpNode(node, op_token, right)

        return node

    # term -> factor ((MUL | DIV) factor)*
    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            op_token = self.current_token
            self.advance()
            right = self.factor()
            node = BinOpNode(node, op_token, right)

        return node

    # factor -> NUMBER | LPAREN expr RPAREN
    def factor(self):
        tok = self.current_token

        if tok.type == NUMBER:
            self.advance()
            return NumberNode(tok.value)

        if tok.type == LPAREN:
            self.advance()
            node = self.expr()
            if self.current_token.type != RPAREN:
                raise Exception("Missing closing parenthesis")
            self.advance()
            return node

        raise Exception(f"Unexpected token in factor: {tok}")
    

# Evaluator
def eval_node(node):
    if isinstance(node, NumberNode):
        return node.value

    if isinstance(node, BinOpNode):
        left_val = eval_node(node.left)
        right_val = eval_node(node.right)
        t = node.op_token.type

        if t == PLUS:
            return left_val + right_val
        if t == MINUS:
            return left_val - right_val
        if t == MUL:
            return left_val * right_val
        if t == DIV:
            if right_val == 0:
                raise Exception("Error: division by zero") # avoid division by zero
            return left_val / right_val

    raise Exception(f"Unknown node type: {node}")


# Simple REPL (main loop) to test the lexer and parser
while True:
    expr = input(">>> ")
    if expr.strip().lower() in ("exit", "quit"):
        break

    if not expr.strip():
        continue

    lexer = Lexer(expr)
    tokens = lexer.get_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    result = eval_node(tree)
    print(result)
