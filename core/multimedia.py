from abc import ABCMeta
from core.command import CoreException, ICommand, BaseInvoker, CommandErrorCode, InvokerErrorCode, Result
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pynput.keyboard import Controller, Key

class Multimedia(BaseInvoker):
    def __init__(self) -> None:
        self.commands = {
            "volume": Volume(),
            "track": Track()
        }

class Volume(ICommand):
    def __init__(self) -> None:
        self.devices = AudioUtilities.GetSpeakers()
        interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = cast(interface, POINTER(IAudioEndpointVolume))

    @property
    def volume(self):
        return self._volume.GetMasterVolumeLevel()

    def execute(self, *args, **kwargs) -> Result:
        volume = kwargs.get('volume')
        if volume is None:
            return Result.from_error(CoreException(
                CommandErrorCode.MISSING_ARGUMENT,
                'Missing argument: Missing volume'
            ))

        return Result.from_value(self._set_volume(volume))

    def _set_volume(self, volume: float):
        # Ensure the volume is between 0.0 and 1.0
        volume = max(0.0, min(100.0, volume)) / 100.0
        self._volume.SetMasterVolumeLevelScalar(volume, None)
        return self.volume

class Track(ICommand):
    def __init__(self) -> None:
        self.keyboard = Controller()
        self.mapping = {
            "playpause": self._playpause,
            "next": self._next,
            "prev": self._prev
        }

    def execute(self, *args, **kwargs) -> Result:
        action = kwargs.get('action')
        if action is None:
            return Result.from_error(CoreException(
                CommandErrorCode.MISSING_ARGUMENT,
                'Missing argument: Missing action'
            ))

        if action not in self.mapping:
            return Result.from_error(CoreException(
                CommandErrorCode.INVALID_ARGUMENT,
                f'Invalid argument: {action}'
            ))

        self.mapping[action]()
        return Result.from_value(0)

    def _playpause(self):
        self.keyboard.press(Key.media_play_pause)
        self.keyboard.release(Key.media_play_pause)

    def _next(self):
        self.keyboard.press(Key.media_next)
        self.keyboard.release(Key.media_next)

    def _prev(self):
        self.keyboard.press(Key.media_previous)
        self.keyboard.release(Key.media_previous)