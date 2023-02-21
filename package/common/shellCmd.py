import subprocess

class shellCmd():
    def __init__(self):
        self.cmd = subprocess

    def execute(self, command, *args, **kwargs):
        return self.cmd.run(command, *args, **kwargs)