import unittest
import sys
from unittest import result

sys.path.append("src")

from syntax import parse


class TestParser(unittest.TestCase):
    def test_0_arg_command(self):
        cmdline = "command"
        result = parse(cmdline)
        self.assertEqual(result, [["command"]])

    def test_single_arg_command(self):
        cmdline = "command argument"
        result = parse(cmdline)
        self.assertEqual(result, [["command", "argument"]])

    def test_multi_arg_command(self):
        cmdline = "command argument argument argument argument argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument", "argument", "argument", "argument", "argument"]],
        )

    def test_seq_with_0_arg(self):
        cmdline = "command argument ; command"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument"], ["command"]],
        )

    def test_seq_with_single_arg(self):
        cmdline = "command argument ; command argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument"], ["command", "argument"]],
        )

    def test_seq_with_multi_arg(self):
        cmdline = (
            "command argument argument argument argument argument ; command argument"
        )
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                ["command", "argument", "argument", "argument", "argument", "argument"],
                ["command", "argument"],
            ],
        )

    def test_multi_seq(self):
        cmdline = "command argument ; command ; command argument argument argument; command argument argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                ["command", "argument"],
                ["command"],
                ["command", "argument", "argument", "argument"],
                ["command", "argument", "argument"],
            ],
        )

    def test_pipe_with_0_arg(self):
        cmdline = "command argument | command"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument", """`'"|""", "command"]],
        )

    def test_pipe_with_single_arg(self):
        cmdline = "command argument | command argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument", """`'"|""", "command", "argument"]],
        )

    def test_pipe_with_multi_arg(self):
        cmdline = (
            "command argument argument argument argument argument | command argument"
        )
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                [
                    "command",
                    "argument",
                    "argument",
                    "argument",
                    "argument",
                    "argument",
                    """`'"|""",
                    "command",
                    "argument",
                ]
            ],
        )

    def test_multiple_pipe_with_single_arg_command(self):
        cmdline = "command argument | command argument | command argument | command argument | command argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                [
                    "command",
                    "argument",
                    """`'"|""",
                    "command",
                    "argument",
                    """`'"|""",
                    "command",
                    "argument",
                    """`'"|""",
                    "command",
                    "argument",
                    """`'"|""",
                    "command",
                    "argument",
                ]
            ],
        )

    def test_pipe_with_0arg_command_1arg_command_and_multi_arg_command(self):
        cmdline = "command argument | command | command argument argument argument argument argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                [
                    "command",
                    "argument",
                    """`'"|""",
                    "command",
                    """`'"|""",
                    "command",
                    "argument",
                    "argument",
                    "argument",
                    "argument",
                    "argument",
                ]
            ],
        )

    def test_sub_with_command_outside_sub(self):
        cmdline = "command `command argument`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", """`'\"""", ["command", "argument"]]],
        )

    def test_sub_with_command_inside_sub(self):
        cmdline = "`command command` argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["""`'\"""", ["command", "command"], "argument"]],
        )

    def test_sub_with_seq_inside_sub(self):
        cmdline = "command `command argument ; command argument`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                [
                    "command",
                    """`'\"""",
                    ["command", "argument", """`'";""", "command", "argument"],
                ]
            ],
        )

    def test_sub_with_pipe_inside_sub(self):
        cmdline = "command `command argument | command argument`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [
                [
                    "command",
                    '`\'"',
                    ["command", "argument", """`'"|""", "command", "argument"],
                ]
            ],
        )

    def test_in_rdr(self):
        cmdline = "command < argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", """`'"<""", "argument"]],
        )

    def test_in_rdr_with_reverse_order(self):
        cmdline = "< argument command"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["""`'"<""", "argument", "command"]],
        )

    def test_in_rdr_with_other_arg(self):
        cmdline = "command argument < argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument", """`'"<""", "argument"]],
        )

    def test_out_rdr(self):
        cmdline = "command > argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", """`'">""", "argument"]],
        )

    def test_out_rdr_with_other_arg(self):
        cmdline = "command argument > argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", "argument", """`'">""", "argument"]],
        )

    def test_in_out_rdr(self):
        cmdline = "command < argument > argument"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", """`'"<""", "argument", """`'">""", "argument"]],
        )

    def test_sub_without_arguement(self):
        cmdline = "command `command`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [["command", """`'\"""", ["command"]]],
        )

    def test_sub_with_multiple_seq(self):
        cmdline = "command `command arguement ; command arguement ; command arguement ; command arguement ; command arguement`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [['command', """`'\"""", ['command', 'arguement', """`'";""", 'command', 'arguement', """`'";""", 'command', 'arguement', """`'";""", 'command', 'arguement', """`'";""", 'command', 'arguement']]],
        )

    def test_sub_with_redirectout(self):
        cmdline = "command `command arguement > arguement`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [['command', '`\'"', ['command', 'arguement', '`\'">', 'arguement']]],
        )

    def test_sub_with_redirectin(self):
        cmdline = "command `command arguement < arguement`"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [['command', '`\'"', ['command', 'arguement', '`\'"<', 'arguement']]],
        )

    def test_sub_in_arg(self):
        cmdline = "command arguement`command arguement`arguement"
        result = parse(cmdline)
        self.assertEqual(
            result,
            [['command', 'arguement', '`\'"p', '`\'"', ['command', 'arguement'], '`\'"p', 'arguement']],
        )

    def test_sub_in_arg_quoted(self):
        cmdline = 'command "arguement`command "arguement"`arguement"'
        result = parse(cmdline)
        self.assertEqual(
            result,
            [['command', 'arguement', '`\'"p', '`\'"', ['command', 'arguement'], '`\'"p', 'arguement']],
        )

if __name__ == "__main__":
    unittest.main()
