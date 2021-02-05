from django.core.management import call_command
from django.db.utils import OperationalError


class TestsCommands:
    def test_wait_for_db_is_ready(self, mocker):
        mocked_function = mocker.patch('django.db.utils.ConnectionHandler.__getitem__',
                                       return_value=True)
        call_command('wait_for_db')
        mocked_function.assert_called_once()

    def test_wait_for_db_to_be_ready(self, mocker):
        mocker.patch('time.sleep', return_value=True)
        mocked_function = mocker.patch('django.db.utils.ConnectionHandler.__getitem__',
                                       side_effect=[OperationalError] * 5 + [True])
        call_command('wait_for_db')
        assert mocked_function.call_count == 6
