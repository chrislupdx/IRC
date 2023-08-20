import unittest
import socket
from unittest.mock import MagicMock, call, PropertyMock, Mock, patch
from client import Client
import pytest

class MockSocket:
    def __init__(self):
        pass

    def connect(self, *args, **kwargs):
        raise Exception("Connection failed")

def test_run_pass(mocker):
    # arrange
    client_mock = Client("localhost", 8080)
    t = MagicMock()
    t.start = MagicMock()

    # act
    client_res = client_mock.run() 

    # assert
    assert client_res == 1

def test_run_socket_fail(mocker):
    #arrange
    host = "localhost"
    port = 8080

    #simulate a socket failure
    mock_socket = MagicMock()
    mock_socket.socket = MagicMock(socket.socket)
    mock_socket.connect.side_effect = socket.error("Simulated error")
    
    with patch("client.socket", new=mock_socket):
        client = Client(host, port)

        #act
        exit_code = client.run()

        #assert
        assert exit_code == 1

def test_readsocket(mocker):
    #what conditions would we want to test
    # mock the socket 
    # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # #create the client object
    # testclient = Client()
    # #feed client a socket
    # #produce the mocked result
    # #wait readSocket woudle need to return something
    # assert test_client(self.s) == client
    # return 0
    pass

#could do a suit eof these
def test_parseusercommand(mocker):
    #if you "/connect localhost 8080"
    #you should expect a Connect(localhost 8080)
    #there would be around 9 options you could take
    pass



def test_readInput(mocker):
    #has 8 params
    pass


def test_do_get(mocker):
    # Mocking the SFTPClient instance and the pysftp.Connection instance
    # client_mock = SFTPClient()
    # connection_mock = MagicMock()

    # # Mocking the get method of the pysftp.Connection instance
    # connection_mock.get = MagicMock()

    # # Setting the client attribute of the SFTPClient instance to the mocked pysftp.Connection instance
    # client_mock.client = connection_mock

    # # Mocking os.path.basename to always return 'localfile'
    # mocker.patch('sftp_client.client.os.path.basename', return_value='localfile')

    # # Mocking print function
    # print_mock = mocker.patch('builtins.print')

    # # Call the method
    # client_mock.do_get('remotefile localfile')

    # # Assert it called get method on pysftp.Connection instance with correct arguments
    # assert connection_mock.get.call_args == call('remotefile', 'localfile')

    # # Assert the successful download print
    # assert print_mock.call_args == call('File downloaded successfully')
    pass
    # readsocket
    # run
    # parseusercommand
    # parseservermessage
    # execute servermessage
    # readinput
    #



def test_parseServerMessage(mocker):
    pass
    #there are four possible parameeters

def test_executeServerMessage(mocker):
    #has 4 params
    pass