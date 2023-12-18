from core.command import ICommand, BaseInvoker, CommandErrorCode, CommandError, Result
import screen_brightness_control as sbc
import os
import platform

class System(BaseInvoker):
    def __init__(self) -> None:
        self.COMMANDS = {
            "sleep": Sleep(),
            "shutdown": Shutdown(),
        }

class Sleep(ICommand):
    # The actual system calls being made via the os module
    SLEEP_COMMANDS = {
        "instant": {
            "linux": "systemctl suspend",
            "windows": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
        },
        "deferred": {
            "linux": "echo 'systemctl suspend' | at now + {} minutes",
            "windows": "timeout /t {} /nobreak && rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
        }
    }

    def execute(self, *args, **kwargs) -> Result:
        delay = kwargs.get('delay')
        self._sleep(delay)

    # Sets the delay to the system call string
    # and executes it via the os module
    def _sleep(self, delay=None):
        os_type = self.get_os()
        if delay is None:
            command = self.SLEEP_COMMANDS['instant'][os_type]
        else:
            command = self.SLEEP_COMMANDS['deferred'][os_type] \
            .format(delay * 60 if os_type == 'windows' else delay)

        os.system(command)

    @staticmethod
    def get_os():
        return 'windows' if platform.system() == 'Windows' else 'linux'

class Shutdown(ICommand):
    def execute(self, *args, **kwargs):
        return os.system("shutdown /s /t 1")