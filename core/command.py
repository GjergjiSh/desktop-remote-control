from abc import ABC, abstractmethod

class Command(ABC):
    id: str

    @abstractmethod
    def execute(self, *args, **kwargs) -> int:
        pass


class Invoker(ABC):
    commands: dict[str, Command]

    @abstractmethod
    def invoke(self, command_id: str, *args, **kwargs) -> int:
        pass

    def add_command(self, command: Command) -> None:
        self.commands[command.id] = command

    def remove_command(self, command_id: str) -> None:
        if command_id in self.commands:
            del self.commands[command_id]