from core.command import Command, Invoker
import os

class System(Invoker):
    def __init__(self) -> None:
        self.commands = {
            "sleep": Sleep(),
            "print": Print()
        }

    def invoke(self, command_id: str, *args, **kwargs):
        return self.commands[command_id].execute(*args, **kwargs)

class Sleep(Command):
    def execute(self, *args, **kwargs):
        self._sleep()

    def _sleep(self):
        return os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

class Print(Command):
    def execute(self, *args, **kwargs):
        print("Hello World")