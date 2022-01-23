import appTemplate
from typing import List


class Cat(appTemplate.AppTemplate):
    def __cat_single(self, path: str) -> List[str]:
        result = []
        with open(path) as f:
            result += f.readlines()
        return result

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

        if stdin and not args:
            # in bash, stdin is only used when no commandline args.
            stdout.clear()
            for i in stdin:
                # cat lines from stdin directly.
                stdout.append(i if i and i[-1] != '\n' else i[:-1])
            return 0
        result: List[str] = []
        for a in args:
            try:
                result += self.__cat_single(a)
            except FileNotFoundError:
                stdout.clear()
                return 1
        stdout.clear()
        for i in result:
            stdout.append(i if i and i[-1] != '\n' else i[:-1])
        return 0


__app__ = Cat()
