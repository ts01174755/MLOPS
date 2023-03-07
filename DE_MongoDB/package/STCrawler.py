from package.common.bs4Crawler import bs4Crawler

class STCrawler():
    def __init__(self):
        pass

    def get_st_all_data(self):
        # 獲取網頁回應
        crawler = bs4Crawler()
        crawlerSoup = crawler.get_soup('http://roma254-1.kddns.info:8022/Course/AdminCourses.php')
        print(crawlerSoup)

        return crawlerSoup