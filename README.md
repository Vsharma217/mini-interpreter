# Mini Interpreter

A hand-built interpreter for a small, custom programming language, 
written in Python from scratch. It takes source code through a full interpreter pipeline: 
scanning, parsing, and evaluation, executing programs with variables, 
arithmetic, conditionals, and output.

This project was built to apply concepts from compiler design and automata theory in a hands-on way — implementing a lexer, a 
recursive descent parser, and a tree-walking evaluator entirely by 
hand.

## Supports
- Variables
  - ex: `var x = 5`
- Arithmetic
  - `( )`
  - `*`, `/`
  - `+`, `-`
- Comparisons
  - `==`
  - `<`, `>`
- Conditionals
  - `if`
  - `if / else`
  - nested `if / else`
- Printing
  - `print` statement

Does not support loops or functions.

## Project Structure
- `token_types.py` — token type definitions
- `scanner.py` — lexer, converts source into tokens
- `ast_nodes.py` — AST node classes (expressions and statements)
- `parser.py` — recursive descent parser
- `environment.py` — variable storage
- `evaluator.py` — tree-walking evaluator
- `run_file.py` — entry point, runs a program file

## Architecture
Source Code → Scanner → Parser → Evaluator

### Scanner
Converts the source code into a list of Tokens (e.g. `NUMBER`, `PLUS`, `IDENTIFIER`).

### Parser
Takes the tokens and checks them against the grammar, building an 
Abstract Syntax Tree (AST) using recursive descent.

### Evaluator
Walks the AST and actually runs the program — assigning variables, 
evaluating expressions, and executing statements like `print` and `if`.

## Grammar

The grammar below defines the language's syntax. Rules are ordered by 
precedence — lower rules bind tighter (evaluated first), higher rules 
bind looser, which is what makes expressions like `2 + 3 * 4` parse 
and evaluate correctly.

```expression → equality
equality → comparison ( "==" comparison )*
comparison → term ( ( "<" | ">" ) term )*
term → factor ( ( "+" | "-" ) factor )*
factor → unary ( ( "*" | "/" ) unary )*
unary → "-" unary | primary
primary → NUMBER | IDENTIFIER | "(" expression ")"

program → statement* EOF
statement → varDecl | printStmt | ifStmt | exprStmt
varDecl → "var" IDENTIFIER "=" expression
printStmt → "print" expression
ifStmt → "if" expression statement ( "else" statement )?
exprStmt → expression
```

## Example: 
Program:
```var x = 5
var y = 10
if x > y print 1 else if x<y print 2
var z = x + y
print z
if z == 15 print 99
```
Output:
```2.0
15.0
99.0
```

### How to run: 
`python run_file.py test_program.txt`
*Note: Needs Python 3 installed, no external dependencies.*

## Design Notes

The parser is hand-written using recursive descent rather than a
generated parser (e.g. LALR/yacc-style). This was intentional — the
grammar is small enough not to need a parser generator, and writing
it by hand means every part of the pipeline is fully understood and
debuggable rather than relying on a generated, opaque parse table.

While building this, I found and fixed real bugs, including an
operator-precedence bug (the right-hand side of `+`/`-` was calling
the wrong grammar rule, breaking expressions like `2 + 3 * 4`) and a
logic bug in token-matching that silently broke end-of-input
detection.