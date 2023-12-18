from core.command import CoreException, ICommand, BaseInvoker, CommandErrorCode, InvokerErrorCode, Result
import screen_brightness_control as sbc
import os
import platform

class System(BaseInvoker):
    def __init__(self) -> None:
        self.commands = {
            "sleep": Sleep(),
        }

class Sleep(ICommand):
    # The actual system calls being made via the os module
    # to put the system to sleep
    SYSTEM_CALLS = {
        "sleep": {
            "instant": {
                "linux": "systemctl suspend",
                "windows": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
            },
            "deferred": {
                "linux": "echo 'systemctl suspend' | at now + {} minutes",
                "windows": "timeout /t {} /nobreak && rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
            }
        },
        "shutdown": {
            "instant": {
                "linux": "shutdown -h now",
                "windows": "shutdown /s /t 1"
            },
            "deferred": {
                "linux": "shutdown -h +{}",
                "windows": "shutdown /s /t {}"
            }
        }
    }

    def execute(self, *args, **kwargs) -> Result:
        delay = kwargs.get('delay')
        request_type = kwargs.get('type')

        if request_type is None:
            return Result.from_error(CoreException(
                CommandErrorCode.MISSING_ARGUMENT,
                'Missing argument: Missing request type'
            ))

        if request_type == 'sleep':
            return Result.from_value(self._sleep(delay))
        elif request_type == 'shutdown':
            return Result.from_value(self._shutdown(delay))
        else:
            return Result.from_error(CoreException(
                CommandErrorCode.INVALID_ARGUMENT,
                f'Invalid argument: {request_type}'
            ))

    # Sets the delay to the system call string
    # and executes it via the os module
    def _sleep(self, delay=None):
        os_type = self._get_os()
        if delay is None or delay == 0:
            command = self.SYSTEM_CALLS['sleep']['instant'][os_type]
        else:
            command = self.SYSTEM_CALLS['sleep']['deferred'][os_type] \
            .format(delay * 60 if os_type == 'windows' else delay)

        return os.system(command)

    def _shutdown(self, delay=None):
        os_type = self._get_os()
        if delay is None:
            command = self.SYSTEM_CALLS['shutdown']['instant'][os_type]
        else:
            command = self.SYSTEM_CALLS['shutdown']['deferred'][os_type] \
            .format(delay * 60 if os_type == 'windows' else delay)

        return os.system(command)

    @staticmethod
    def _get_os():
        return 'windows' if platform.system() == 'Windows' else 'linux'

    def _set_system_calls(self, system_calls : dict):
        self.SYSTEM_CALLS = system_calls