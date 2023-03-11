import requests

class STCrawler():
    def __init__(self):
        pass

    def get_st_all_data(self, URL, cookies=None):

        # 獲取網頁回應
        crawlerRes = requests.get(URL, cookies=cookies)
        return crawlerRes.text

    def mongodb_insert_document(self, mongoDBCtrl, collection, document):
        mongoDBCtrl.insert_document(collection, document)

        return 'success'