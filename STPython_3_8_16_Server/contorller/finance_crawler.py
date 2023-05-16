from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


class FinanceCrawler:
    def __init__(self):
        pass

    def get_futures_data(self, get_futures_data_url, app_path):
        driver = webdriver.Chrome(app_path)
        driver.get(get_futures_data_url)
        time.sleep(3)

        # 尋找按鈕並點擊
        approve_wrap = driver.find_element(By.CLASS_NAME, 'approve-wrap')
        confirm_button = approve_wrap.find_element(By.CLASS_NAME, 'btn')
        confirm_button.click()
        while True:
            # 等待數秒讓 JavaScript 資料載入
            time.sleep(5)

            # 透過 BeautifulSoup 解析網頁內容
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'class': 'table quotes-table mb-1 sticky-table-horizontal'})

            # 獲取資料欄位名稱
            thead = table.find('thead')
            thead_th = thead.find_all('th')
            thead_cols = [th_.getText() for th_ in thead_th]
            # print(thead_cols)

            # 獲取資料內容
            tbody = table.find('tbody')
            tbody_trs = tbody.find_all('tr')
            tbody_data = []
            for tr_ in tbody_trs:
                tbody_trs_tds = tr_.find_all('td')
                tbody_trs_data = [td_.getText().strip() for td_ in tbody_trs_tds]
                tbody_data.append(tbody_trs_data)
            # print(tbody_data)

            # 將資料轉換為 DataFrame
            futures_df = pd.DataFrame(tbody_data, columns=thead_cols)
            print(futures_df)

            # driver.quit()     # 關閉瀏覽器


if __name__ == "__main__":
    # 盤後交易行情
    FinanceCrawler().get_futures_data(
        get_futures_data_url="https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/FuturesDomestic/",
        app_path="/Applications/Google\ Chrome.app"
    )

    # 一般交易行情
    FinanceCrawler().get_futures_data(
        get_futures_data_url="https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/FuturesDomestic/",
        app_path="/Applications/Google\ Chrome.app"
    )