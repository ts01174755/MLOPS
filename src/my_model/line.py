import requests
import os.path


class LineNotify:
    def __init__(self, token):
        self.token = token

    def send(self, message):  # 傳送文字訊息
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"message": message}
        r = requests.post(
            "https://notify-api.line.me/api/notify", headers=headers, data=data
        )
        return r.status_code


if __name__ == "__main__":
    import json

    # 取得 token
    with open("MLOPS/env/LineNotify.json", "r") as f:
        lineNotifyToken = json.load(f)

    lineNotify = LineNotify(lineNotifyToken["token"])
    lineNotify.send("Hello World")
