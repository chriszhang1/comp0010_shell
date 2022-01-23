import appTemplate
import os
from typing import List


class Sort(appTemplate.AppTemplate):
    def exec(self,
             raw_args: List[str],
             stdin: List[str],
             stdout: List[str]) -> int:

        args = []
        for i in raw_args:
            expanded = self.gen_wildcard_matches(i)
            if expanded == []:
                args.append(i)
            else:
                args.extend(expanded)

        stdout.clear()
        argument = args
        reverse = False
        if "-r" in argument:
            reverse = True
            argument.remove("-r")
        if len(argument) == 0:
            argument = stdin
        if len(argument) < 1:
            # both stdin and args are empty.
            return 1
        if len(argument) == 1 and os.path.isfile(argument[0]):
            with open(argument[0], "r") as f:
                argument = f.readlines()
        argument.sort(reverse=reverse)

        for i in argument:
            if i[-1] == "\n":
                i = i[:-1]
            stdout.append(i)
        return 0


__app__ = Sort()
