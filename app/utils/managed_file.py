class ManagedFile:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args

    def __enter__(self):
        self.file = open(self.name, self.args)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
