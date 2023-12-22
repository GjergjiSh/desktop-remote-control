from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class Result(Generic[T]):
    def __init__(self, value: Optional[T] = None, error: Optional[Exception] = None):
        self._value = value
        self._error = error

    @property
    def value(self) -> Optional[T]:
        return self._value

    @property
    def error(self) -> Optional[Exception]:
        return self._error

    def succeded(self) -> bool:
        return self._error is None

    def failed(self) -> bool:
        return self._error is not None

    @staticmethod
    def from_value(value: T) -> 'Result':
        return Result(value=value)

    @staticmethod
    def from_error(error: Exception) -> 'Result':
        return Result(error=error)

class ICommand(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        raise NotImplementedError

class BaseInvoker():
    commands : dict[str,ICommand]

    def __init__(self) -> None:
        self.commands = {}

    def invoke(self, command_id: str, *args, **kwargs) -> Result:
        if command_id not in self.commands:
            return Result.from_error(CoreException(
                InvokerErrorCode.INVALID_COMMAND,
                f'Command {command_id} does not exist'
            ))

        return self.commands[command_id].execute(*args, **kwargs)

    def add_command(self, command_id: str, command: ICommand) -> Result:
        self.commands[command_id] = command
        return Result.from_value(command)

    def remove_command(self, command_id: str) -> None:
        if command_id not in self.commands:
            return Result.from_error(CoreException(
                InvokerErrorCode.INVALID_COMMAND,
                f'Command {command_id} does not exist'
            ))

        del self.commands[command_id]

class CommandErrorCode(Enum):
    INVALID_ARGUMENT = 1
    MISSING_ARGUMENT = 2

class InvokerErrorCode(Enum):
    INVALID_COMMAND = 1

ErrorCode = TypeVar('ErrorCode', bound=Enum)

class CoreException(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code.name}: {self.message}'