from unittest.mock import MagicMock, call, PropertyMock
from client import client

def test_run(mocker):
    pass
    #run also doesn't return anything of signififcance


def test_do_get(mocker):
    # Mocking the SFTPClient instance and the pysftp.Connection instance
    client_mock = SFTPClient()
    connection_mock = MagicMock()

    # Mocking the get method of the pysftp.Connection instance
    connection_mock.get = MagicMock()

    # Setting the client attribute of the SFTPClient instance to the mocked pysftp.Connection instance
    client_mock.client = connection_mock

    # Mocking os.path.basename to always return 'localfile'
    mocker.patch('sftp_client.client.os.path.basename', return_value='localfile')

    # Mocking print function
    print_mock = mocker.patch('builtins.print')

    # Call the method
    client_mock.do_get('remotefile localfile')

    # Assert it called get method on pysftp.Connection instance with correct arguments
    assert connection_mock.get.call_args == call('remotefile', 'localfile')

    # Assert the successful download print
    assert print_mock.call_args == call('File downloaded successfully')

# readsocket
# run
# parseusercommand
# parseservermessage
# execute servermessage
# readinput
#

def test_readsocket(mocker):
    #what conditions would we want to test
    # mock the socket 
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #create the client object
    testclient = Client()
    #feed client a socket
    #produce the mocked result
    #wait readSocket woudle need to return something
    assert test_client(self.s) == client
    

#could do a suit eof these
def test_parseusercommand(mocker):
    #if you "/connect localhost 8080"
    #you should expect a Connect(localhost 8080)
    #there would be around 9 options you could take
    pass

def test_parseServerMessage(mocker):
    pass
    #there are four possible parameeters

def test_executeServerMessage(mocker):
    #has 4 params
    pass

def test_readInput(mocker):
    #has 8 params
    pass