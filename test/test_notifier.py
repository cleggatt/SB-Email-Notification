import os
import sys

# Could also run the tests with the environment variable "PYTHONPATH=../."
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from mock import call
from mock import patch
from mock import Mock
from sbnotify.notifier import *


@patch('smtplib.SMTP')
def test_email(mock_smtp_constructor):
    # Set up
    mock_smtp = Mock(name='SMTP mock')
    mock_smtp_constructor.return_value = mock_smtp

    notifier = EmailNotifier('Series name', 2, 42,
                             {'mail_server': 'mail.com',
                              'mail_port': '123',
                              'mail_account': 'me@mail.com',
                              'mail_password': 's3cr3t',
                              'mail_to': 'recipient@mail.com',
                              'mail_from': 'sender@mail.com'})
    # Test
    notifier.notify()
    # Verify
    mock_smtp_constructor.assert_called_with('mail.com', '123')
    # Compare calls individually to make spotting errors easier
    assert mock_smtp.method_calls[0] == call.ehlo()
    assert mock_smtp.method_calls[1] == call.starttls()
    assert mock_smtp.method_calls[2] == call.login('me@mail.com', 's3cr3t')
    assert mock_smtp.method_calls[3] == call.sendmail('sender@mail.com',
                                                      'recipient@mail.com',
                                                      ('From: sender@mail.com\r\n' +
                                                       'Subject: New episode of Series name\r\n' +
                                                       'To: recipient@mail.com\r\n' +
                                                       'MIME-Version: 1.0\r\n' +
                                                       'Content-Type: text/html\r\n\r\n' +
                                                       'A new episode of Series name is available (Season 2, episode 42)'))
    assert mock_smtp.method_calls[4] == call.quit()
    assert len(mock_smtp.method_calls) == 5


@patch('httplib2.Http.request')
def test_todo(mock_request):
    # Set up
    notifier = TodoNotifier('Series name', 2, 42, {'todo_api_key': '2143'})
    # Test
    notifier.notify()
    # Verify
    mock_request.assert_called_with('https://todoist.com/API/addItem?token=2143&content=Watch+Series+name%2C+episode+42+from+season+2', 'GET')
