import appTemplate
from typing import List
import os


class Head(appTemplate.AppTemplate):
    def __head(self,
               lines: List[str],
               number: int = 10) -> List[str]:
        result: List[str] = []
        for i in range(number):
            if i < len(lines):
                result.append(lines[i])
            else:
                break
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

        result = []
        number = 10
        if len(args) == 1 and os.path.isfile(args[0]):
            # passing file from command line with no options
            with open(args[0], "r") as file:
                result = self.__head(file.readlines(), number)
        elif len(stdin) > 0:
            # passing file from stdin.
            if len(args) == 2 and args[0] == "-n":
                try:
                    number = int(args[1])
                except ValueError:
                    return 1
            elif len(args) == 0:
                number = 10
            else:
                return 1
            result = self.__head(stdin.copy(), number)
        elif len(args) == 3 and args[0] == '-n' and os.path.isfile(args[2]):
            # passing file from argument.
            try:
                number = int(args[1])
            except ValueError:
                return 1
            with open(args[2], "r") as file:
                result = self.__head(file.readlines(), number)
        else:
            return 1
        stdout.clear()
        stdout.extend([i if i[-1] != '\n' else i[:-1] for i in result])
        return 0


__app__ = Head()
