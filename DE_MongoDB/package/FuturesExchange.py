import requests
import subprocess
class FuturesExchange():
    def __init__(self):
        pass

    def get_futuresExchange_dailyFile(self, URL, FILEPATH):
        # 獲取網頁回應
        crawlerRes = requests.get(URL, allow_redirects=True)
        open(FILEPATH, 'wb').write(crawlerRes.content)
        subprocess.run(f"unzip -o {FILEPATH} -d {'/'.join(FILEPATH.split('/')[:-1])}", shell=True)
        subprocess.run(f"rm {FILEPATH}", shell=True)
        return 'success'