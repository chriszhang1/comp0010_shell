import appTemplate
from typing import List


class Unsafe(appTemplate.AppTemplate):
    def __init__(self, app: appTemplate.AppTemplate):
        self.__app = app

    def exec(self,
             args: List[str],
             stdin: List[str],
             stdout: List[str]):
        self.__app.exec(args, stdin, stdout)
        # whatever the return code of the execution is,
        # return 0 (no error) so that the sequence is not interrupted.
        return 0
