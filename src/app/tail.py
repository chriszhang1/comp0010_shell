import os
import appTemplate
from typing import List


class Tail(appTemplate.AppTemplate):
    def __tail(self, lines: List[str], number: int = 10) -> List[str]:
        result: List[str] = []
        for i in range(len(lines) - 1, -1, -1):
            try:
                if number > 0:
                    result.append(lines[i])
                    number -= 1
                else:
                    break
            except IndexError:
                break
        result.reverse()
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
            # passing file from argument with no options
            with open(args[0], "r") as file:
                lines = file.readlines()
                result = self.__tail(lines, number)

        elif len(stdin) > 1:
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
            result = self.__tail(stdin.copy(), number)

        elif len(args) == 3 and args[0] == "-n":
            # passing file from argument
            try:
                number = int(args[1])
            except ValueError:
                stdout.clear()
                return 1
            with open(args[2], "r") as file:
                lines = file.readlines()
                result = self.__tail(lines, number)
        else:
            stdout.clear()
            return 1
        stdout.clear()
        stdout.extend(i if i and i[-1] != "\n" else i[:-1] for i in result)
        return 0


__app__ = Tail()
