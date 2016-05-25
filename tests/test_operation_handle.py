import pytest

from mock import MagicMock, call

from dcss.server import OperationHandle


@pytest.fixture
def operation():
    dcss = MagicMock()
    return OperationHandle(dcss, 'robot_config', '123.45')


def test_operation_handle_repr(operation):
    assert repr(operation) == "<OperationHandle [123.45]: robot_config>"


def test_operation_completed(operation):
    operation.operation_completed('ok', 'done')
    expected = call('htos_operation_completed robot_config 123.45 normal ok done')
    assert operation.dcss.send_xos3.call_args == expected


def test_operation_error(operation):
    operation.operation_error('bad', 'bad')
    expected = call('htos_operation_completed robot_config 123.45 error bad bad')
    assert operation.dcss.send_xos3.call_args == expected


def test_operation_update(operation):
    operation.operation_update('good', 'so', 'far')
    expected = call('htos_operation_update robot_config 123.45 good so far')
    assert operation.dcss.send_xos3.call_args == expected
