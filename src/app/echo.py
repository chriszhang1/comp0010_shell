import appTemplate
from typing import List


class Echo(appTemplate.AppTemplate):
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

        result = [' '.join(i.lstrip().rstrip() for i in args)]
        stdin.clear()
        stdout.clear()
        for i in result:
            stdout.append(i)
        return 0


__app__ = Echo()
