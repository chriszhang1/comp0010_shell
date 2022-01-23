import re
import appTemplate
from typing import List


class Grep(appTemplate.AppTemplate):
    def __grep(self,
               pattern: re.Pattern,
               sources: List[str]) -> List[str]:
        result: List[str] = []
        for line in sources:
            if pattern.match(line):
                if line[-1] == '\n':
                    line = line[:-1]
                result.append(line)
        return result

    def exec(self,
             args: List[str],
             stdin: List[str],
             stdout: List[str]) -> int:
        stdout.clear()
        if len(args) < 2 and not (len(args) == 1 and stdin):
            return 1
        pattern_str = self.peel_quote(args[0])
        if pattern_str[0] != '^':
            pattern_str = '.*' + pattern_str
        pattern = re.compile(pattern_str)

        if len(args) >= 2:
            files: List[str] = []
            for i in args[1:]:
                files.extend(self.gen_wildcard_matches(i))
            if not files:
                return 1

            for file in files:
                with open(file) as f:
                    result = self.__grep(pattern, f.readlines())
                    if len(files) > 1:
                        # prepend filename if there are multiple files.
                        result = [file + ":" + i for i in result]
                    stdout.extend(result)

        elif len(args) == 1 and stdin:
            stdout.clear()
            stdout.extend(self.__grep(pattern, stdin.copy()))

        else:
            stdout.clear()
            return 1

        return 0


__app__ = Grep()
