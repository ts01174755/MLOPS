import subprocess

class shellCmd():
    def __init__(self):
        self.cmd = subprocess

    def execute(self, command, *args, **kwargs):
        return self.cmd.run(command, *args, **kwargs)

    # 把指令結果回傳成String
    def getoutput(self, command, *args, **kwargs):
        return self.cmd.getoutput(command, *args, **kwargs)