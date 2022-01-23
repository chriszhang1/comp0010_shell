import glob
from typing import List


class AppTemplate:
    def exec(self,
             args: List[str],
             stdin: List[str],
             stdout: List[str]) -> int:
        '''
        Return value:
            0: the app is executed normally.
            Any other non-zero value: the app is running abnormally.
        '''
        return 0

    def peel_quote(self, string: str) -> str:
        # remove the quotation marks around a string.
        if string \
                and string[0] == string[-1] \
                and (string[0] == "'" or string[0] == '"'):
            return string[1:-1]
        return string

    def gen_wildcard_matches(self,
                             wildcard: str,
                             recursive: bool = True) -> List[str]:
        # generate recursive wildcard matches from string.
        return glob.glob(self.peel_quote(wildcard), recursive=recursive)
