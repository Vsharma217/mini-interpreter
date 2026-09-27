from scanner import Scanner
from parser import Parser
from evaluator import Evaluator
from environment import Environment
import sys

def run_file(path):
    with open(path, "r") as f:
        source = f.read()
    env = Environment()
    evaluator = Evaluator(env)
    for line in source.strip().split("\n"):
        line =line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            tokens = Scanner(line).scan_tokens()
            statements = Parser(tokens).parse()
            evaluator.run(statements)
        except (SyntaxError, RuntimeError) as e:
            print(f"Error: {e}")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_file.py <path_to_program>")
    else:
        run_file(sys.argv[1])