from core.command import Command, Invoker
import screen_brightness_control as sbc
import os

class System(Invoker):
    def __init__(self) -> None:
        self.commands = {
            "sleep": Sleep(),
            "shutdown": Shutdown(),
        }

    def invoke(self, command_id: str, *args, **kwargs):
        return self.commands[command_id].execute(*args, **kwargs)

class Sleep(Command):
    def execute(self, *args, **kwargs):
        return os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

class Shutdown(Command):
    def execute(self, *args, **kwargs):
        return os.system("shutdown /s /t 1")