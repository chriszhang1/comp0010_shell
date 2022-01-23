import os
import appTemplate
from typing import List


class Ls(appTemplate.AppTemplate):
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
        result: List[str] = []
        ls_dir = str()
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1 or not os.path.isdir(args[0]):
            return 1
        else:
            ls_dir = args[0]
        for f in os.listdir(ls_dir):
            if not f.startswith("."):
                result.append(f)

        stdout.clear()
        # print function has newline symbol as suffix so don't add it here.
        stdout.append('\t'.join(result))
        return 0


__app__ = Ls()
