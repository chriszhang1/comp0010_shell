import sys
from typing import List
import unittest
import os

sys.path.append('./src')
from app import \
    cat, cd, exit, echo, ls, cut, pwd, find, grep, head, sort, tail, uniq
import unsafe


_cat = cat.Cat()
_cd = cd.Cd()
_exit = exit.Exit()
_echo = echo.Echo()
_ls = ls.Ls()
_cut = cut.Cut()
_pwd = pwd.Pwd()
_find = find.Find()
_grep = grep.Grep()
_head = head.Head()
_sort = sort.Sort()
_tail = tail.Tail()
_uniq = uniq.Uniq()

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


class TestApps(unittest.TestCase):

    def test_echo(self):
        cmdline = ["hello", "world"]
        stdout = []
        _echo.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["hello world"])

    def test_ls(self):
        cmdline = []
        stdout: List[str] = []
        _ls.exec(cmdline, [], stdout)
        result = set(stdout[0].replace('\n', '').split('\t'))
        self.assertEqual(result, set(i for i in os.listdir() if i[0] != '.'))

    def test_ls_error(self):
        cmdline = ['dir1', 'dir2']
        stdout = []
        self.assertNotEqual(0, _ls.exec(cmdline, [], stdout))

    def test_ls_dir(self):
        cmdline = ["dir1"]
        stdout = []
        _ls.exec(cmdline, [], stdout)
        result = set(stdout[0].replace('\n', '').split('\t'))
        self.assertEqual(result, {"file1.txt", "file2.txt", "longfile.txt"})

    def test_ls_hidden(self):
        cmdline = ["dir2/subdir"]
        stdout = []
        _ls.exec(cmdline, [], stdout)
        result = set(stdout[0].replace('\n', '').split('\t'))
        self.assertEqual(result, {"file.txt"})

    def test_pwd(self):
        cmdline = []
        stdout = []
        _pwd.exec(cmdline, [], stdout)
        result = stdout[0]
        self.assertEqual(result, os.getcwd())

    def test_cat(self):
        cmdline = ["dir1/file1.txt", "dir1/file2.txt"]
        stdout = []
        _cat.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "BBB", "AAA", "CCC"])

    def test_cat_missing_file(self):
        cmdline = ['dir3/fhsdjafweao.txt']
        stdout = []
        self.assertNotEqual(0, _cat.exec(cmdline, [], stdout))

    def test_cat_stdin(self):
        cmdline = []
        stdin = ["AAA", "BBB", "AAA"]
        stdout = []
        _cat.exec(cmdline, stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "BBB", "AAA"])

    def test_head(self):
        cmdline = ["dir1/longfile.txt"]
        stdout = []
        _head.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 11)])

    def test_head_stdin(self):
        cmdline = []
        stdin = [str(i) for i in range(1, 11)]
        stdout = []
        _head.exec(cmdline, stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 11)])

    def test_head_stdin_with_args(self):
        cmdline = ['-n', '5']
        stdin = [str(i) for i in range(1, 11)]
        stdout = []
        _head.exec(cmdline, stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 6)])
        cmdline[1] = 'a'
        self.assertNotEqual(0, _head.exec(cmdline, stdin, stdout))

    def test_head_with_wrong_opt(self):
        cmdline = ['-n', 'a']
        stdin = [str(i) for i in range(1, 11)]
        stdout = []
        self.assertNotEqual(0, _head.exec(cmdline, stdin, stdout))

    def test_head_stdin_n5(self):
        cmdline = ['-n', '5']
        stdin = [str(i) for i in range(1, 6)]
        stdout = []
        _head.exec(cmdline, stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 6)])

    def test_head_n5_with_wrong_args(self):
        cmdline = ["-n", "a", "dir1/longfile.txt"]
        stdout = []
        self.assertNotEqual(0, _head.exec(cmdline, [], stdout))

    def test_head_n5(self):
        cmdline = ["-n", "5", "dir1/longfile.txt"]
        stdout = []
        _head.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 6)])

    def test_head_n50(self):
        cmdline = ["-n", "50", "dir1/longfile.txt"]
        stdout = []
        _head.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 21)])

    def test_head_n0(self):
        cmdline = ["-n", "0", "dir1/longfile.txt"]
        stdout = []
        _head.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [])

    def test_tail(self):
        cmdline = ["dir1/longfile.txt"]
        stdout = []
        _tail.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(11, 21)])

    def test_tail_stdin(self):
        cmdline = []
        stdin = [str(i) for i in range(11, 21)]
        stdout = []
        _tail.exec(cmdline, stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(11, 21)])

    def test_tail_stdin_with_args(self):
        cmdline = ['-n', '5']
        stdin = [str(i) for i in range(11, 21)]
        stdout = []
        _tail.exec(cmdline, stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(16, 21)])
        cmdline[1] = 'a'
        self.assertNotEqual(0, _tail.exec(cmdline, stdin, stdout))

    def test_tail_stdin_with_wrong_opt(self):
        cmdline = ['-n', 'a']
        stdin = ["dir1/longfile.txt"]
        stdout = []
        self.assertNotEqual(0, _tail.exec(cmdline, stdin, stdout))

    def test_tail_with_wrong_opt(self):
        cmdline = ['-n', 'a', 'dir1/longfile.txt']
        stdout = []
        self.assertNotEqual(0, _tail.exec(cmdline, [], stdout))

    def test_tail_stdin_with_missing_opt(self):
        cmdline = ['-n']
        stdin = ['dir1/longfile.txt']
        stdout = []
        self.assertNotEqual(0, _tail.exec(cmdline, [], stdout))

    def test_tail_with_excessive_opt(self):
        cmdline = ['-n', 'a', 'dir1/longfile.txt', 'ufsahdufa']
        stdout = []
        self.assertNotEqual(0, _tail.exec(cmdline, [], stdout))

    def test_tail_n5(self):
        cmdline = ["-n", "5", "dir1/longfile.txt"]
        stdout = []
        _tail.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(16, 21)])

    def test_tail_n50(self):
        cmdline = ["-n", "50", "dir1/longfile.txt"]
        stdout = []
        _tail.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [str(i) for i in range(1, 21)])

    def test_tail_n0(self):
        cmdline = ["-n", "0", "dir1/longfile.txt"]
        stdout = []
        _tail.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [])

    def test_grep(self):
        cmdline = ["AAA", "dir1/file1.txt"]
        stdout = []
        _grep.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "AAA"])

    def test_grep_missing_file(self):
        cmdline = ["AAA", "dir3/fsdijlfhjawe.txt"]
        stdout = []
        self.assertNotEqual(0, _grep.exec(cmdline, [], stdout))

    def test_grep_no_matches(self):
        cmdline = ["DDD", "dir1/file1.txt"]
        stdout = []
        _grep.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, [])

    def test_grep_re(self):
        cmdline = ["'A..'", "dir1/file1.txt"]
        stdout = []
        _grep.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "AAA"])

    def test_grep_files(self):
        cmdline = ["'...'", "dir1/file1.txt", "dir1/file2.txt"]
        stdout = []
        _grep.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(
            result,
            [
                "dir1/file1.txt:AAA",
                "dir1/file1.txt:BBB",
                "dir1/file1.txt:AAA",
                "dir1/file2.txt:CCC",
            ],
        )

    def test_grep_stdin(self):
        cmdline = ['dir1/file1.txt', "dir1/file2.txt"]
        stdout = []
        _cat.exec(cmdline, [], stdout)
        cmdline = ["'...'"]
        _grep.exec(cmdline, stdout.copy(), stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "BBB", "AAA", "CCC"])

    def test_sort(self):
        cmdline = ["dir1/file1.txt"]
        stdout = []
        _sort.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "AAA", "BBB"])

    def test_sort_stdin(self):
        stdin = ["dir1/file1.txt"]
        stdout = []
        _sort.exec([], stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "AAA", "BBB"])

    def test_sort_r(self):
        cmdline = ["-r", "dir1/file1.txt"]
        stdout = []
        _sort.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["BBB", "AAA", "AAA"])

    def test_uniq(self):
        cmdline = ["dir2/subdir/file.txt"]
        stdout = []
        _uniq.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "aaa", "AAA"])

    def test_uniq_missing_file(self):
        cmdline = ['dir3/fhsdjafweao.txt']
        stdout = []
        self.assertNotEqual(0, _uniq.exec(cmdline, [], stdout))

    def test_uniq_stdin(self):
        stdin = ["dir2/subdir/file.txt"]
        stdout = []
        _uniq.exec([], stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "aaa", "AAA"])

    def test_sort_uniq(self):
        cmdline = ["dir1/file1.txt"]
        stdout = []
        _sort.exec(cmdline, [], stdout)
        cmdline = []
        _uniq.exec(cmdline, stdout.copy(), stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "BBB"])

    def test_uniq_i(self):
        cmdline = ["-i", "dir2/subdir/file.txt"]
        stdout = []
        _uniq.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA"])

    def test_cut(self):
        cmdline = ["-b", "1", "dir1/file1.txt"]
        stdout = []
        _cut.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["A", "B", "A"])

    def test_cut_missing_file(self):
        cmdline = ["-b", "1", "dir3/file1.txt"]
        stdout = []
        self.assertNotEqual(0, _cut.exec(cmdline, [], stdout))

    def test_cut_wrong_opts(self):
        cmdline = ["-b", "dir3/file1.txt"]
        stdout = []
        self.assertNotEqual(0, _cut.exec(cmdline, [], stdout))

    def test_cut_interval(self):
        cmdline = ["-b", "2-3", "dir1/file1.txt"]
        stdout = []
        _cut.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AA", "BB", "AA"])

    def test_cut_open_interval(self):
        cmdline = ["-b", "2-", "dir1/file1.txt"]
        stdout = []
        _cut.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AA", "BB", "AA"])

    def test_cut_overlapping(self):
        cmdline = ["-b", "2-,3-", "dir1/file1.txt"]
        stdout = []
        _cut.exec(cmdline, [], stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AA", "BB", "AA"])

    def test_cut_stdin(self):
        cmdline = ['abc']
        stdout = []
        _echo.exec(cmdline, [], stdout)
        cmdline = ['-b', '1']
        _cut.exec(cmdline, stdout.copy(), stdout)
        result = stdout.copy()
        self.assertEqual(result, ["a"])

    def test_cut_union(self):
        cmdline = ['abc']
        stdout = []
        _echo.exec(cmdline, [], stdout)
        cmdline = ['-b', '-1,2-']
        _cut.exec(cmdline, stdout.copy(), stdout)
        result = stdout.copy()
        self.assertEqual(result, ["abc"])

    def test_find(self):
        cmdline = ["-name", "file.txt"]
        stdout = []
        _find.exec(cmdline, [], stdout)
        result = set(stdout)
        self.assertEqual(result, {"./dir2/subdir/file.txt"})

    def test_find_error(self):
        cmdline = ["file.txt"]
        stdout = []
        self.assertNotEqual(0, _find.exec(cmdline, [], stdout))

    def test_find_no_opts(self):
        cmdline = ["file.txt"]
        stdout = []
        self.assertNotEqual(0, _find.exec(cmdline, [], stdout))

    def test_find_no_pattern(self):
        cmdline = ["file.txt", "-name"]
        stdout = []
        self.assertNotEqual(0, _find.exec(cmdline, [], stdout))

    def test_find_excessive_args(self):
        cmdline = ["file.txt", 'hfjaskhfs', "-name"]
        stdout = []
        self.assertNotEqual(0, _find.exec(cmdline, [], stdout))

    def test_find_pattern(self):
        cmdline = ["-name", "'*.txt'"]
        stdout = []
        _find.exec(cmdline, [], stdout)
        result = set(stdout)
        self.assertEqual(
            result,
            {
                "./dir2/subdir/file.txt",
                "./test.txt",
                "./dir1/file1.txt",
                "./dir1/file2.txt",
                "./dir1/longfile.txt",
                "./requirements.txt"
            },
        )

    def test_find_dir(self):
        cmdline = ["dir1", "-name", "'*.txt'"]
        stdout = []
        _find.exec(cmdline, [], stdout)
        result = set(stdout)
        self.assertEqual(
            result, {"dir1/file1.txt", "dir1/file2.txt", "dir1/longfile.txt"}
        )

    def test_globbing_dir(self):
        cmdline = ["dir1/*.txt"]
        stdout = []
        _echo.exec(cmdline, [], stdout)
        result = set(stdout[0].replace('\n', '').split())
        self.assertEqual(
            result, {"dir1/file1.txt", "dir1/file2.txt", "dir1/longfile.txt"}
        )

    def test_unsafe_ls(self):
        cmdline = ["dir3"]
        stdout = []
        code = unsafe.Unsafe(_ls).exec(cmdline, [], stdout)
        self.assertEqual(code, 0)

    def test_pipe_uniq(self):
        stdin = ['AAA', 'BBB', 'AAA', 'aaa']
        stdout = []
        _uniq.exec(['-i'], stdin, stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "BBB", "AAA"])

    def test_pipe_chain_sort_uniq(self):
        cmdline = ["dir1/file1.txt", "dir1/file2.txt"]
        stdout = []
        _cat.exec(cmdline, [], stdout)
        cmdline = []
        _sort.exec(cmdline, stdout.copy(), stdout)
        _uniq.exec(cmdline, stdout.copy(), stdout)
        result = stdout.copy()
        self.assertEqual(result, ["AAA", "BBB", "CCC"])
    
    def test_cd(self):
        cwd = os.getcwd()
        cmdline = ['/']
        stdout = []
        _cd.exec(cmdline, [], stdout)
        _pwd.exec(cmdline, [], stdout)
        new_cwd = stdout[0]
        self.assertEqual(new_cwd, '/')
        _cd.exec([cwd], [], stdout)

    def test_cd_home(self):
        cwd = os.getcwd()
        cmdline = []
        stdout = []
        _cd.exec(cmdline, [], stdout)
        _pwd.exec(cmdline, [], stdout)
        new_cwd = stdout[0]
        self.assertEqual(new_cwd, os.path.expanduser('~'))
        _cd.exec([cwd], [], stdout)

    def test_cd_excessive_args(self):
        cmdline = ['/', '.']
        stdout = []
        self.assertNotEqual(0, _cd.exec(cmdline, [], stdout))

    def test_cd_error(self):
        cmdline = ['hjkfsahd']
        self.assertNotEqual(0, _cd.exec(cmdline, [], []))

    def test_exit(self):
        try:
            self.assertEqual(None, _exit.exec([], [], []))
        except SystemExit:
            pass


if __name__ == "__main__":
    unittest.main()
