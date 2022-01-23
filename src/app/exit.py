import appTemplate
import sys


class Exit(appTemplate.AppTemplate):
    def exec(self, *args):
        # an elegant way to exit the shell.
        sys.exit()


__app__ = Exit()
