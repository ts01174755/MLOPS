import requests
from bs4 import BeautifulSoup

class bs4Crawler():
    def __init__(self):
        pass

    # 獲取網頁回應
    @classmethod
    def get_res(cls, url):
        res = requests.get(url)
        return res

    # 獲取網頁內容
    @classmethod
    def get_soup(cls, res):
        soup = BeautifulSoup(res, 'html.parser')
        return soup

    # 解析特定id內容
    @classmethod
    def get_data_id(cls, soup, id):
        data = soup.find(id=id)
        return data

    # 解析特定id內容的文字
    @classmethod
    def get_data_id_text(cls, soup, id):
        data = soup.find(id=id)
        data_text = data.text
        return data_text

    # 解析特定標籤下所有內容
    @classmethod
    def get_data_tag(cls, soup, tag):
        data = soup.find_all(tag)
        return data

    # 解析特定標籤下所有內容的文字
    @classmethod
    def get_data_tag_text(cls, soup, tag):
        data = soup.find_all(tag)
        data_text = [i.text for i in data]
        return data_text

    # 解析特定標籤下所有內容的連結
    @classmethod
    def get_data_href(cls, soup, tag):
        data = soup.find_all(tag)
        data_href = [i['href'] for i in data]
        return data_href

    # 解析特定標籤下所有內容的連結與文字
    @classmethod
    def get_data_href_text(cls, soup, tag):
        data = soup.find_all(tag)
        data_href_text = [(i['href'], i.text) for i in data]
        return data_href_text
