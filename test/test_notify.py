import os
import sys


# Could also run the tests with the env variable "PYTHONPATH=../."
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import pytest
from sbnotify import notify

@pytest.mark.parametrize('path,expected',
                         [
                             ('/foo/bar.mp4', 'bar.mp4'),
                             ('baz.mp4', 'baz.mp4'),
                         ])
def test_episode_name(path, expected):
    assert notify.episode_name(path) == expected
