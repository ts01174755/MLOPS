
from src.model.line import LineNotify

class STLineNotify():

    def __init__(self):
        pass

    def postLineNotify(self, token, message):
        # 取得 token

        lineNotify = LineNotify(token)
        lineNotify.send(message)

        return 'success'
