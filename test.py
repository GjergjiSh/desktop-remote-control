import unittest
from core.command import BaseInvoker, ICommand, Result, CoreException, CommandErrorCode, InvokerErrorCode

class TestCommand(ICommand):
    # Executing the test command with a filter argument returns a the filter as a Result value
    # Executing the test command with no arguments returns an an error as a Result error
    def execute(self, *args, **kwargs):
        filter = kwargs.get('filter', -1)
        return self._execute(filter)

    def _execute(self, filter: int):
        # If no filter was provided, return an error
        if filter == -1:
            return Result.from_error(CoreException(
                CommandErrorCode.INVALID_ARGUMENT,
                'Invalid argument'
            ))

        # Otherwise, return the filter as a value
        return Result.from_value(filter)

class TestBaseInvoker(unittest.TestCase):
    def setUp(self):
        self.invoker = BaseInvoker()
        command = TestCommand()
        self.invoker.add_command('test', command)

    def test_add_command(self):
        # Added by the setUp method
        self.assertTrue('test' in self.invoker.commands)

        # Add a new command
        test_cmd = TestCommand()
        cmd_result = self.invoker.add_command('test2', test_cmd)
        # Check that the command was added
        self.assertTrue(cmd_result.succeded())
        self.assertTrue('test2' in self.invoker.commands)
        self.assertEqual(cmd_result.value, test_cmd)

    def test_invoke_success(self):
        # Invoke with arguments
        result = self.invoker.invoke('test', filter=1)
        # Check that the result is a success and that the value is 1
        self.assertTrue(result.succeded())
        self.assertEqual(result.value, 1)

    def test_invoke_failure(self):
        # Invoke with no arguments
        result = self.invoker.invoke('test')
        self.assertTrue(result.failed())
        # Check that the result is a failure and that the error code and message are correct
        self.assertEqual(result.error.code, CommandErrorCode.INVALID_ARGUMENT)
        self.assertEqual(result.error.message, 'Invalid argument')

    def test_remove_command(self):
        # Remove the test command
        self.invoker.remove_command('test')
        # Check that the command was removed
        self.assertFalse('test' in self.invoker.commands)

        # Try to remove a command that does not exist
        result = self.invoker.remove_command('test2')
        # Check that the result is a failure and that the error code and message are correct
        self.assertTrue(result.failed())
        self.assertEqual(result.error.code, InvokerErrorCode.INVALID_COMMAND)
        self.assertEqual(result.error.message, 'Command test2 does not exist')


if __name__ == '__main__':
    unittest.main()