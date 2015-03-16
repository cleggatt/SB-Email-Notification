import os
import sys

# Could also run the tests with the environment variable "PYTHONPATH=../."
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import pytest
import ConfigParser
from mock import patch, MagicMock
from sbnotify import notify

@patch('httplib2.Response')
@patch('httplib2.Http.request')
def test_series_name(mock_request, mock_response):
    # Set up
    config = ConfigParser.ConfigParser()
    config.get = MagicMock(return_value='8967')
    series_id = '1423'
    response = mock_response()
    mock_request.return_value = (response, '<Data><Series><SeriesName>TV series</SeriesName></Series></Data>')
    # Test
    series_name = notify.series_name(config, series_id)
    # Verify
    mock_request.assert_called_with('http://thetvdb.com/api/8967/series/1423', 'GET')
    assert series_name == 'TV series'


@pytest.mark.parametrize('path,expected',
                         [
                             ('/foo/bar.mp4', 'bar.mp4'),
                             ('baz.mp4', 'baz.mp4'),
                         ])
def test_episode_name(path, expected):
    assert notify.episode_name(path) == expected