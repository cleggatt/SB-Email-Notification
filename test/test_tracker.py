import os
import sys

# Could also run the tests with the environment variable "PYTHONPATH=../."
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import shutil
import tempfile

from mock import patch
from sbnotify.tracker import *


def setup_module(module):
    global temp_dir
    temp_dir = tempfile.mkdtemp()


def teardown_function(function):
    global temp_dir
    if os.path.isfile(temp_dir + '/tracker.dat'):
        os.remove(temp_dir + '/tracker.dat')


def teardown_module(module):
    global temp_dir
    shutil.rmtree(temp_dir)


def test_notification_required:
    pass


@patch('time.time')
def test_process_complete_no_history(mock_time):
    global temp_dir, temp_file, temp_fd
    # Setup
    mock_time.return_value = 1394954792.5
    # Exercise
    Tracker(temp_dir).process_complete('/some/path/file.mp4')
    # Verify
    # TODO Assert file closed
    with open(temp_dir + '/tracker.dat', 'r') as f:
        content = f.read()
    assert content == '{"/some/path/file.mp4": "1394954792.5"}'


@patch('time.time')
def test_process_complete_with_history(mock_time):
    # Setup
    mock_time.return_value = 1394954792.5
    with open(temp_dir + '/tracker.dat', 'w') as f:
        f.write('{"/first/path/file.mp4": "1294954792.5", "/second/path/file.mp4": "1304954792.5"}')
    # Exercise
    Tracker(temp_dir).process_complete('/some/path/file.mp4')
    # Verify
    # TODO Assert file closed
    with open(temp_dir + '/tracker.dat', 'r') as f:
        content = f.read()
    assert content == ('{"/first/path/file.mp4": "1294954792.5", ' +
                       '"/some/path/file.mp4": "1394954792.5", '
                       '"/second/path/file.mp4": "1304954792.5"}')