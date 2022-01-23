import appTemplate
import os
from typing import List


class Uniq(appTemplate.AppTemplate):
    def __uniq(self, content: List[str], insensitive: bool) -> List[str]:
        result = []
        index = 0
        while index < len(content):
            if result == []:
                result.append(content[index])
                index += 1
            elif insensitive:
                if content[index].lower() != result[-1].lower():
                    result.append(content[index])
                index += 1
            else:
                if content[index] != result[-1]:
                    result.append(content[index])
                index += 1
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

        content = []

        case_insensitive = False
        file_path = ''
        content = []
        if '-i' in args:
            args.remove('-i')
            case_insensitive = True
        if len(stdin) == 1 and os.path.isfile(stdin[0]):
            file_path = stdin[0]
        elif len(stdin):
            content = stdin
        elif len(args) == 1 and os.path.isfile(args[0]):
            file_path = args[0]
        else:
            stdout.clear()
            return 1
        if content == []:
            with open(file_path) as f:
                content = [i[:-1] if i[-1] == '\n' else i
                           for i in f.readlines()]

        result: List[str] = self.__uniq(content, case_insensitive)
        stdout.clear()
        for i in result:
            if i[-1] == '\n':
                stdout.append(i[:-1])
            else:
                stdout.append(i)
        return 0


__app__ = Uniq()
