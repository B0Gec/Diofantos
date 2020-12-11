import sys

"""Solution class for copying output to log file; copied from
https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file/616686#616686
"""

class Tee(object):
    def __init__(self, name, mode="w"):
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
        # print("Destructor __del__ was called inside SO's Tee.")
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        self.file.flush()
        self.stdout.flush()
