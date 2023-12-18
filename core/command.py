from abc import ABC, abstractmethod
from enum import Enum
from concurrent.futures import Future
from typing import Generic, TypeVar, Union, Optional

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        self._value = value
        self._error = error

    @property
    def value(self) -> Optional[T]:
        return self._value

    @property
    def error(self) -> Optional[E]:
        return self._error

    def is_ok(self) -> bool:
        return self._error is None

    def is_error(self) -> bool:
        return self._error is not None

    def from_value(self, value: T) -> 'Result':
        self._value = value
        return self

    def from_error(self, error: E) -> 'Result':
        self._error = error
        return self


class ICommand(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        raise NotImplementedError

class IAsyncCommand(ABC):
    future: Future

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Future:
        raise NotImplementedError

class BaseInvoker():
    commands : dict[str,ICommand]

    def __init__(self) -> None:
        self.commands = {}

    def invoke(self, command_id: str, *args, **kwargs) -> Result:
        if command_id not in self.commands:
            raise CommandError(
                CommandErrorCode.INVALID_ARGUMENT,
                f'Command {command_id} does not exist'
            )

        return self.commands[command_id].execute(*args, **kwargs)

    def add_command(self, command_id: str, command: ICommand) -> None:
        self.commands[command_id] = command

    def remove_command(self, command_id: str) -> None:
        if command_id not in self.commands:
            raise CommandError(
                CommandErrorCode.INVALID_ARGUMENT,
                f'Command {command_id} does not exist'
            )

        del self.commands[command_id]

class BaseAsyncInvoker():
    commands : dict[str,IAsyncCommand]

    def __init__(self) -> None:
        self.commands = {}

    async def invoke(self, command_id: str, *args, **kwargs) -> None:
        if command_id not in self.commands:
            raise CommandError(
                CommandErrorCode.INVALID_ARGUMENT,
                f'Command {command_id} does not exist'
            )

        self.commands[command_id].execute(*args, **kwargs)

    def add_command(self, command_id: str, command: IAsyncCommand) -> None:
        self.commands[command_id] = command

    def remove_command(self, command_id: str) -> None:
        if command_id not in self.commands:
            raise CommandError(
                CommandErrorCode.INVALID_ARGUMENT,
                f'Command {command_id} does not exist'
            )

        del self.commands[command_id]

class CommandErrorCode(Enum):
    INVALID_ARGUMENT = 1

class CommandError(Exception):
    def __init__(self, domain: CommandErrorCode, message: str):
        self.domain = domain
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.domain.name}: {self.message}'