import os
import appTemplate
from typing import List


class Cd(appTemplate.AppTemplate):
    def exec(self,
             raw_args: List[str],
             stdin: List[str],
             stdout: List[str]) -> int:
        stdout.clear()
        args = []
        for i in raw_args:
            expanded = self.gen_wildcard_matches(i)
            if expanded == []:
                args.append(i)
            else:
                args.extend(expanded)
        if args == []:
            # default to home directory.
            args.append(os.path.expanduser('~'))
        if len(args) != 1:
            # too much arguments.
            return 1
        elif not os.path.isdir(args[0]):
            # not a directory
            return 1
        os.chdir(args[0])
        return 0


__app__ = Cd()
