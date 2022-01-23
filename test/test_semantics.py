import os
import unittest
import subprocess
from src import semantics, syntax
from lark import exceptions

for i in ('dir1', 'dir2', 'test.txt', 'newfile.txt'):
    if i in os.listdir():
        os.system(f"rm -rf {i}")

filesystem_setup = ";".join(
    [
        "echo \"''\" > test.txt",
        "mkdir dir1",
        "mkdir dir2"
        "mkdir -p dir2/subdir",
        "echo AAA > dir1/file1.txt",
        "echo BBB >> dir1/file1.txt",
        "echo AAA >> dir1/file1.txt",
        "echo CCC > dir1/file2.txt",
        "echo 1 > dir1/longfile.txt",
        "for i in `seq 2 20`; do echo $i >> dir1/longfile.txt; done",
        "echo AAA > dir2/subdir/file.txt",
        "echo aaa >> dir2/subdir/file.txt",
        "echo AAA >> dir2/subdir/file.txt",
        "touch dir2/subdir/.hidden",
    ]
)
os.system(filesystem_setup)


class TestEval(unittest.TestCase):
    def eval(self, cmd, shell='/comp0010/sh'):
        if shell == '/comp0010/sh':
            stdin, stdout = [], []
            try:
                p_out = syntax.parse(cmd)
            except exceptions.UnexpectedCharacters \
                    or exceptions.UnexpectedToken \
                    or exceptions.UnexpectedEOF:
                stdout.clear()
                print("Syntax Error")
            else:
                return_code = semantics.evaluate(p_out, stdin, stdout)
            return '\n'.join(stdout)
        else:
            return ''.join(i for i in os.popen(cmd).readlines())
    
    def test_unsupported(self):
        app_name = 'hasfueao'
        self.assertEqual(self.eval(app_name).split(' ')[:3], ['Unsupported', 'application', app_name])

    def test_cat_stdin(self):
        cmdline = "cat < dir1/file1.txt"
        stdout = self.eval(cmdline)
        result = stdout.strip().split("\n")
        self.assertEqual(result, ["AAA", "BBB", "AAA"])

    def test_grep_stdin(self):
        cmdline = "cat dir1/file1.txt dir1/file2.txt | grep '...'"
        stdout = self.eval(cmdline)
        result = stdout.strip().split("\n")
        self.assertEqual(result, ["AAA", "BBB", "AAA", "CCC"])

    def test_input_redirection_infront(self):
        cmdline = "< dir1/file2.txt cat"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "CCC")

    def test_input_redirection_nospace(self):
        cmdline = "cat <dir1/file2.txt"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "CCC")

    def test_output_redirection(self):
        cmdline = "echo foo > newfile.txt"
        self.eval(cmdline)
        stdout = self.eval("cat newfile.txt", shell="/bin/bash")
        result = stdout.strip()
        self.assertEqual(result, "foo")

    def test_output_redirection_overwrite(self):
        cmdline = "echo foo > test.txt"
        self.eval(cmdline)
        stdout = self.eval("cat test.txt", shell="/bin/bash")
        result = stdout.strip()
        self.assertEqual(result, "foo")
        self.eval("echo \"''\" >  test.txt", shell="/bin/bash")

    def test_semicolon(self):
        cmdline = "echo AAA; echo BBB"
        stdout = self.eval(cmdline)
        result = set(stdout.strip().split())
        self.assertEqual(result, {"AAA", "BBB"})

    def test_semicolon_chain(self):
        cmdline = "echo AAA; echo BBB; echo CCC"
        stdout = self.eval(cmdline)
        result = set(stdout.strip().split())
        self.assertEqual(result, {"AAA", "BBB", "CCC"})

    def test_semicolon_exception(self):
        cmdline = "ls dir3; echo BBB"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "")

    def test_unsafe(self):
        cmdline = "_ls dir3; echo AAA > newfile.txt"
        self.eval(cmdline)
        stdout = self.eval("cat newfile.txt", shell="/bin/sh")
        result = stdout.strip()
        self.assertEqual(result, "AAA")

    def test_pipe_uniq(self):
        cmdline = (
            "echo aaa > dir1/file2.txt; cat dir1/file1.txt dir1/file2.txt | uniq -i"
        )
        stdout = self.eval(cmdline)
        result = stdout.strip().split("\n")
        self.assertEqual(result, ["AAA", "BBB", "AAA"])

    def test_pipe_chain_sort_uniq(self):
        cmdline = "cat dir1/file1.txt dir1/file2.txt | sort | uniq"
        stdout = self.eval(cmdline)
        result = stdout.strip().split("\n")
        self.assertEqual(result, ["AAA", "BBB", "CCC"])
    
    def test_substitution(self):
        cmdline = "echo `echo foo`"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "foo")

    def test_substitution_insidearg(self):
        cmdline = "echo a`echo a`a"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "aaa")

    def test_substitution_splitting(self):
        cmdline = "echo `echo foo  bar`"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "foo bar")

    def test_substitution_sort_find(self):
        cmdline = "cat `find dir2 -name '*.txt'` | sort"
        stdout = self.eval(cmdline)
        result = stdout.strip().split("\n")
        self.assertEqual(result, ["AAA", "AAA", "aaa"])

    def test_substitution_semicolon(self):
        cmdline = "echo `echo foo; echo bar`"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "foo bar")

    def test_substitution_keywords(self):
        cmdline = "echo `cat test.txt`"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "''")

    def test_substitution_app(self):
        cmdline = "`echo echo` foo"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "foo")

    def test_singlequotes(self):
        cmdline = "echo 'a  b'"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "a  b")

    def test_quote_keyword(self):
        cmdline = "echo ';'"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, ";")

    def test_doublequotes(self):
        cmdline = 'echo "a  b"'
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "a  b")

    def test_substitution_doublequotes(self):
        cmdline = 'echo "`echo foo`"'
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "foo")

    def test_nested_doublequotes(self):
        cmdline = 'echo "a `echo "b"`"'
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "a b")

    def test_disabled_doublequotes(self):
        cmdline = "echo '\"\"'"
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, '""')

    def test_splitting(self):
        cmdline = 'echo a"b"c'
        stdout = self.eval(cmdline)
        result = stdout.strip()
        self.assertEqual(result, "abc")


if __name__ == "__main__":
    unittest.main()
