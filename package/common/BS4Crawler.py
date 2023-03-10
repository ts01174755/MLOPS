import requests
from bs4 import BeautifulSoup

class BS4Crawler():
    def __init__(self):
        pass

    # 獲取網頁回應
    @classmethod
    def get_res(cls, url, cookies=None):
        if cookies:
            res = requests.get(url, cookies=cookies)
        else:
            res = requests.get(url)
        return res

    # 獲取網頁內容
    @classmethod
    def get_soup(cls, res):
        if type(res) == str:
            soup = BeautifulSoup(res, 'html.parser')
        else:
            soup = BeautifulSoup(res.text, 'html.parser')
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
    def get_data_tag(cls, soup, tag, attrs=None):
        if attrs:
            data = soup.find_all(tag, attrs=attrs)
        else:
            data = soup.find_all(tag)
        return data

    # 解析特定標籤下所有內容的文字
    @classmethod
    def get_data_tag_text(cls, soup, tag):
        data = soup.find_all(tag)
        data_text = [i.text for i in data]
        return data_text

    # soup 漂亮的印出
    @classmethod
    def print_soup(cls, soup):
        print(soup.prettify())

