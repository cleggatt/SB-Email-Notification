import json
import os
import time


class Tracker(object):

    def __init__(self, base_path):
        self.tracker_file_path = base_path + '/tracker.dat'

        if os.path.isfile(self.tracker_file_path):
            try:
                if os.path.isfile(self.tracker_file_path):
                    f = open(self.tracker_file_path, 'r+')
                    self.data = json.loads(f.read())
                    f.seek(0)
                    f.truncate()
            finally:
                f.close()
        else:
            self.data = {}

    def notification_required(self, path):
        pass

    def process_complete(self, path):
        # TODO Add some better error handling and recover
        try:
            f = open(self.tracker_file_path, 'w')

            now = time.time()
            self.data[path] = '{}'.format(now)

            f.write(json.dumps(self.data))
        finally:
            f.close()