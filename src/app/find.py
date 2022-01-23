import appTemplate
from typing import List
import os


class Find(appTemplate.AppTemplate):
    def exec(self,
             args: List[str],
             stdin: List[str],
             stdout: List[str]) -> int:
        stdout.clear()
        if '-name' not in args:
            return 1

        if args.index('-name') == 0:
            root_dir = "./"
        elif args.index('-name') == 1:
            root_dir = args[0]
        else:
            return 1

        try:
            name_pattern_string = args[args.index('-name') + 1]
        except IndexError or ValueError:
            # fail safe.
            return 1

        stdout += self.gen_wildcard_matches(
                os.path.join(root_dir,
                             '**',
                             self.peel_quote(name_pattern_string)),
                recursive=True)
        return 0


__app__ = Find()
