import os
import appTemplate
from typing import List


class Pwd(appTemplate.AppTemplate):
    def exec(self,
             args: List[str],
             stdin: List[str],
             stdout: List[str]) -> int:
        stdout.clear()
        stdout.append(os.getcwd())
        return 0


__app__ = Pwd()
