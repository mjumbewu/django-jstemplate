class MockFinder(object):
    def __init__(self, retval=None):
        self.retval = retval


    def find(self, name):
        return self.retval
