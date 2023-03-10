from package.common.BS4Crawler import BS4Crawler

class STCrawler():
    def __init__(self):
        pass

    def get_st_all_data(self, URL, cookies=None):

        # 獲取網頁回應
        crawlerRes = BS4Crawler.get_res(URL, cookies=cookies)
        # print(crawlerRes.text)
        return crawlerRes.text