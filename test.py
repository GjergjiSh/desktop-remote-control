import unittest
from core.command import BaseInvoker, ICommand, Result, CoreException, CommandErrorCode, InvokerErrorCode
from core.system import Sleep

class TestCommand(ICommand):
    def execute(self, *args, **kwargs):
        should_succeed = kwargs.get('should_succeed')
        if should_succeed is False:
            return Result.from_error(CoreException(
                CommandErrorCode.INVALID_ARGUMENT,
                'Invalid argument'
            ))

        return Result.from_value(True)

class TestSleepCommand(unittest.TestCase):
    def setUp(self):
        self.command = Sleep()

        # Mock system calls
        self.command._set_system_calls({
            "sleep": {
                "instant": {
                    "linux": "echo 'systemctl suspend'",
                    "windows": "echo 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'"
                },
                "deferred": {
                    "linux": "echo 'systemctl suspend in {} minutes'",
                    "windows": "echo 'sleep in {} seconds'"
                }
            },
            "shutdown": {
                "instant": {
                    "linux": "echo 'shutdown -h now'",
                    "windows": "echo 'shutdown /s /t 1'"
                },
                "deferred": {
                    "linux": "echo 'shutdown -h in {} minutes'",
                    "windows": "echo 'shutdown /s /t {} seconds'"
                }
            }
        })

    def test_execute_success(self):
        result = self.command.execute(type='sleep')
        self.assertTrue(result.succeded())
        self.assertEqual(result.value, 0)

        result = self.command.execute(type='shutdown')
        self.assertTrue(result.succeded())
        self.assertEqual(result.value, 0)

        result = self.command.execute(type='sleep', delay=1)
        self.assertTrue(result.succeded())
        self.assertEqual(result.value, 0)

        result = self.command.execute(type='shutdown', delay=1)
        self.assertTrue(result.succeded())
        self.assertEqual(result.value, 0)

    def test_execute_failure(self):
        self.assertFalse(self.command.execute(type='invalid').succeded())
        result = self.command.execute(type='invalid')
        self.assertIsNone(result.value)
        self.assertEqual(result.error.code, CommandErrorCode.INVALID_ARGUMENT)
        self.assertEqual(result.error.message, 'Invalid argument: invalid')

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
        result = self.invoker.invoke('test', should_succeed=True)
        # Check that the result is a success and that the value is 0
        self.assertTrue(result.succeded())
        self.assertEqual(result.value, 1)

    def test_invoke_failure(self):
        # Invoke with no arguments
        result = self.invoker.invoke('test', should_succeed=False)
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