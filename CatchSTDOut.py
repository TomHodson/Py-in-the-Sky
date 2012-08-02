import sys

class CatchSTDOut(object):
    def __init__(self, out, err):
        self.out = out; self.err = err
        self.oldstdout = sys.stdout
    def write(self, input):
        self.out.append(input)
        self.oldstdout.write(input)
    def __enter__(self):
        sys.stdout = self
        return self
    def __exit__(self, type, value, traceback):
        sys.stdout = self.oldstdout
        self.err = (type, value, traceback)
        return True
    def __getattr__(self, name):
        return self.oldstdout.__getattr__(name)
