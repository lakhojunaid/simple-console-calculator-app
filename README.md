# Expression Interpreter
A simple Python interpreter that evaluates arithmetic expressions using a real compiler-style pipeline.

# Features
* Supports `+  -  *  /  ^`
* Correct precedence (including exponentiation)
* Parentheses and unary minus
* Lexer → Parser → AST → Evaluator
* Small Read-Evaluate-Print-Loop(REPL) interface (`>>>`)

# Example
>>> 1 + 2 * 3
7
>>> (2 + 3)^2
25
>>> -4 * 5
-20

# Run:
python3 main.py
