# includes parser for the shell.
import os
from lark import Lark
from decodeAST import decompress
from typing import List


lark_path = os.path.realpath(__file__).replace("syntax.py", "grammar.lark")
parser = Lark.open(lark_path)


def parse(cmdline: str) -> List:
    parse_result = decompress(str(parser.parse(cmdline)))
    return parse_result
