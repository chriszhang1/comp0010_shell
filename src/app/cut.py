import appTemplate
from typing import List


class Cut(appTemplate.AppTemplate):
    def __parse_args(self, arg: str, total_length: int) -> List[int]:
        """
        Parses the arguments of the cut command to generate lines to return.
        """
        if total_length == 0:
            return []
        args = arg.split(',')
        result = []
        for i in args:
            if '-' not in i:
                result.append(int(arg) - 1)
            elif i[0] == '-':
                result += [j for j in range(int(i[1:]))]
            elif i[-1] == '-':
                result += [j for j in range(int(i[:-1]) - 1, total_length)]
            else:
                lower, upper = i.split('-')
                result += [j for j in range(int(lower) - 1, int(upper))]
        return sorted(list(set(result)))

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
        lines = []

        if 2 <= len(args) <= 3 and args[0] == '-b':
            arguments = args[1]
            if len(args) == 2:
                if stdin == []:
                    return 1
                lines = stdin.copy()
            else:
                try:
                    with open(args[2]) as f:
                        lines = [i if i[-1] != '\n' else i[:-1]
                                 for i in f.readlines()]

                except FileNotFoundError:
                    return 1
        else:
            stdout.clear()
            return 1
        for i in lines:
            # the following line should work for
            # characters longer than 1 byte.
            byte_string = bytes(i, 'utf8')
            total_length = len(byte_string)
            try:
                line_index = self.__parse_args(arguments, total_length)
            except ValueError:
                return 1

            new_line: str = ""
            for j in line_index:
                new_line += chr(byte_string[j])
            stdout.append(new_line)
        return 0


__app__ = Cut()
