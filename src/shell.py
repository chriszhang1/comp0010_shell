import os
import sys
from typing import List
import semantics
import syntax
from lark import exceptions


def evaluate(command: str) -> List[str]:
    if len(command) == 0 or command.isspace():
        # empty command
        return []

    stdin, stdout = [], []
    try:
        p_out = syntax.parse(command)
    except exceptions.UnexpectedCharacters \
            or exceptions.UnexpectedToken \
            or exceptions.UnexpectedEOF:
        # failed to parse
        stdout.clear()
        print("Syntax Error")
        return stdout
    else:
        return_code = semantics.evaluate(p_out, stdin, stdout)
        if return_code:
            # non-zero return code. execution failed.
            return []
        return stdout


if __name__ == "__main__":
    if '-c' in sys.argv:
        cmdline = sys.argv[sys.argv.index('-c') + 1]
        stdout = evaluate(cmdline)
        for i in stdout:
            print(i)
    else:
        while True:
            try:
                cmdline = input(os.getcwd() + "> ")
                # If user enter nothing, continue to accept input
                stdout = evaluate(cmdline)
                for i in stdout:
                    print(i)
            except KeyboardInterrupt:
                pass
