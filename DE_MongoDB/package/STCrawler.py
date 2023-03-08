from package.common.bs4Crawler import bs4Crawler

class STCrawler():
    def __init__(self):
        pass

    def get_st_all_data(self, URL, cookies=None):

        # 獲取網頁回應
        crawlerRes = bs4Crawler.get_res(URL, cookies=cookies)
        # print(crawlerRes.text)

        # 解析的部分留到下一階段
        # crawlerSoup = bs4Crawler.get_soup(crawlerRes)
        # print(crawlerSoup)
        return crawlerRes.text