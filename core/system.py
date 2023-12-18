from core.command import Command
import os

class System(Command):
    def execute(self, *args, **kwargs):
        self._sleep()

    def _sleep(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


    # COMMANDS = {
    #     "sleep": sleep
    # }