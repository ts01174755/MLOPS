import requests
from bs4 import BeautifulSoup

class bs4Crawler():
    def __init__(self):
        self.res = None
        self.soup = None

    # 獲取網頁回應
    def get_res(self, url):
        self.res = requests.get(url)
        return self.res

    # 獲取網頁內容
    def get_soup(self):
        self.soup = BeautifulSoup(self.res.text, 'lxml')
        return self.soup

    # 解析特定id內容
    def get_data_id(self, id):
        data = self.soup.find(id=id)
        return data

    # 解析特定id內容的文字
    def get_data_id_text(self, id):
        data = self.soup.find(id=id)
        data_text = data.text
        return data_text

    # 解析特定標籤下所有內容
    def get_data(self, tag, attrs):
        data = self.soup.find_all(tag, attrs=attrs)
        return data

    # 解析特定標籤下所有內容的文字
    def get_data_text(self, tag, attrs):
        data = self.soup.find_all(tag, attrs=attrs)
        data_text = [i.text for i in data]
        return data_text

    # 解析特定標籤下所有內容的連結
    def get_data_href(self, tag, attrs):
        data = self.soup.find_all(tag, attrs=attrs)
        data_href = [i['href'] for i in data]
        return data_href

    # 解析特定標籤下所有內容的連結與文字
    def get_data_href_text(self, tag, attrs):
        data = self.soup.find_all(tag, attrs=attrs)
        data_href_text = [(i['href'], i.text) for i in data]
        return data_href_text

