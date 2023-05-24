import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

class FuturesExchangeTW:
    def __init__(self):
        pass

    @classmethod
    def get_call_put_price(cls, desLogPhysicalPrice, exercisePrice, actionRate, noRiskRate, cashStockRate, dayType, period, dayYear):
        payload = {
            "desLogPhysicalPrice": f"{str(desLogPhysicalPrice)}",  # 標的指數現貨價格
            "exercisePrice": f"{str(exercisePrice)}",  # 履約價格
            "actionRate": f"{str(actionRate)}",  # 波動率
            "noRiskRate": f"{str(noRiskRate)}",  # 無風險利率
            "cashStockRate": f"{str(cashStockRate)}",  # 現金股利率
            "dayType": f"{str(dayType)}",  # 存續期間选择
            "period": f"{str(period)}",  # 存續期間（这里的例子是30天）
            "dayYear": f"{str(dayYear)}"  # 存續期間的计算单位
        }
        response = requests.post(
            url="https://www.taifex.com.tw/cht/9/calOptPrice",
            data=payload
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        # 搜尋 class 為 'table_c' 的 table 標籤
        table = soup.find('table', {'class': 'table_c'})

        # 在這個 table 中找到所有的 td 標籤
        tds = table.find_all('td')
        data = {
            tds[0].text.strip().lower(): float(tds[2].text.strip().replace(',', '')),
            tds[1].text.strip().lower(): float(tds[3].text.strip().replace(',', ''))
        }
        return data

    @classmethod
    def get_opt_IV(cls, desLogPhysicalPrice, exercisePrice, noRiskRate, cashStockRate, dayType, period, dayYear, callPut, premium):
        payload = {
            'desLogPhysicalPrice': f"{(desLogPhysicalPrice)}",
            'exercisePrice': f"{(exercisePrice)}",
            'noRiskRate': f"{(noRiskRate)}",
            'cashStockRate': f"{(cashStockRate)}",
            "dayType": f"{(dayType)}",  # 存續期間选择
            "period": f"{(period)}",  # 存續期間（这里的例子是30天）
            'dayYear': f"{(dayYear)}",
            'callPut': f"{(callPut)}".lower(),  # 'call' 或者 'put'
            'premium': f"{(premium)}",  # 將此替換為你的權利金數值
        }

        response = requests.post(
            url="https://www.taifex.com.tw/cht/9/calOptImpliedPrice",
            data=payload
        )
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假設結果在一個包含文字 "隱含波動率:" 的td標籤中
        result = soup.find('td').find_next('u').text
        result = result.replace('%', '')  # 移除百分比符號
        result = float(result)  # 將字串轉換為浮點數

        data = {
            callPut.lower(): {
                'OptImpliedPrice': result
            }
        }
        return data

    @classmethod
    def get_opt_delta(cls, desLogPhysicalPrice, exercisePrice, actionRate, noRiskRate, cashStockRate, dayType, period, dayYear, callPut):
        call_put_price_list = []
        for len_ in range(-1, 2):
            call_put_price_ = FuturesExchangeTW.get_call_put_price(
                desLogPhysicalPrice=desLogPhysicalPrice + len_ * 10,
                exercisePrice=exercisePrice,
                actionRate=actionRate,
                noRiskRate=noRiskRate,
                cashStockRate=cashStockRate,
                dayType=dayType,
                period=period,
                dayYear=dayYear
            )
            call_put_price_list.append(call_put_price_)
        delta = (call_put_price_list[2][callPut] - call_put_price_list[0][callPut])/20
        return round(delta, 4)

    @classmethod
    def get_opt_theta(cls, desLogPhysicalPrice, exercisePrice, actionRate, noRiskRate, cashStockRate, dayType, period, dayYear, callPut):
        call_put_price_list = []
        for len_ in range(2):
            call_put_price_ = FuturesExchangeTW.get_call_put_price(
                desLogPhysicalPrice=desLogPhysicalPrice,
                exercisePrice=exercisePrice,
                actionRate=actionRate,
                noRiskRate=noRiskRate,
                cashStockRate=cashStockRate,
                dayType=dayType,
                period=period - len_,
                dayYear=dayYear
            )
            call_put_price_list.append(call_put_price_)
        theta = (call_put_price_list[0][callPut] - call_put_price_list[1][callPut])
        return round(theta, 4)

class FinanceCrawler:
    def __init__(self):
        pass

    @classmethod
    def get_futures_data(cls, get_futures_data_url, app_path, conn):
        driver = webdriver.Chrome(app_path)
        driver.get(get_futures_data_url)
        time.sleep(3)

        # 尋找按鈕並點擊
        approve_wrap = driver.find_element(By.CLASS_NAME, 'approve-wrap')
        confirm_button = approve_wrap.find_element(By.CLASS_NAME, 'btn')
        confirm_button.click()

        # 等待數秒讓 JavaScript 資料載入
        time.sleep(5)
        while True:
            try:
                # 透過 BeautifulSoup 解析網頁內容
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', {'class': 'table quotes-table mb-1 sticky-table-horizontal'})

                # 獲取資料欄位名稱
                thead = table.find('thead')
                thead_th = thead.find_all('th')
                thead_cols = [th_.getText() for th_ in thead_th]

                # 獲取資料內容
                tbody = table.find('tbody')
                tbody_trs = tbody.find_all('tr')
                tbody_data = []
                for tr_ in tbody_trs:
                    tbody_trs_tds = tr_.find_all('td')
                    tbody_trs_data = [td_.getText().strip() for td_ in tbody_trs_tds]
                    tbody_data.append(tbody_trs_data)

                # 將資料轉換為 DataFrame
                futures_df = pd.DataFrame(tbody_data, columns=thead_cols)

                # send the data frame to the parent process
                # 塞入當今實現還有資料
                conn.send((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), futures_df.to_dict()))

                time.sleep(1)

            except Exception as e:
                print(e)
                time.sleep(1)
                continue
        # driver.quit()     # 關閉瀏覽器

    @classmethod
    def get_opts_data(cls, get_futures_data_url, app_path, conn):
        driver = webdriver.Chrome(app_path)
        driver.get(get_futures_data_url)
        time.sleep(3)

        # 尋找按鈕並點擊
        approve_wrap = driver.find_element(By.CLASS_NAME, 'approve-wrap')
        confirm_button = approve_wrap.find_element(By.CLASS_NAME, 'btn')
        confirm_button.click()
        # 等待數秒讓 JavaScript 資料載入
        time.sleep(5)
        while True:
            try:

                # 透過 BeautifulSoup 解析網頁內容
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', {'class': 'table quotes-table mb-1 options-t sticky-table-horizontal sticky-table-horizontal-2'})

                # 獲取資料欄位名稱
                thead = table.find('thead')
                thead_th = thead.find_all('th')
                thead_cols = [th_.getText() for th_ in thead_th]
                thead_cols_ = [thead_cols[0] + '_' + col_ for col_ in thead_cols[3:10]] +\
                              [thead_cols[10]] +\
                              [thead_cols[2] + '_' + col_ for col_ in thead_cols[11:]]
                thead_cols = thead_cols_

                # 獲取資料內容
                tbody = table.find('tbody')
                tbody_trs = tbody.find_all('tr')
                tbody_data = []
                for tr_ in tbody_trs:
                    tbody_trs_tds = tr_.find_all('td')
                    tbody_trs_data = [td_.getText().strip() for td_ in tbody_trs_tds]
                    tbody_data.append(tbody_trs_data)

                # 將資料轉換為 DataFrame
                futures_df = pd.DataFrame(tbody_data, columns=thead_cols)

                # send the data frame to the parent process
                conn.send((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), futures_df.to_dict()))

                time.sleep(1)
            #  印出錯誤
            except Exception as e:
                print(e)
                time.sleep(1)
                continue

        # driver.quit()     # 關閉瀏覽器


if __name__ == "__main__":
    # # 盤後交易行情
    # FinanceCrawler().get_futures_data(
    #     get_futures_data_url="https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/FuturesDomestic/",
    #     app_path="/Applications/Google\ Chrome.app"
    # )
    #
    # # 一般交易行情
    # FinanceCrawler().get_futures_data(
    #     get_futures_data_url="https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/FuturesDomestic/",
    #     app_path="/Applications/Google\ Chrome.app"
    # )
    # # 盤後交易行情
    FinanceCrawler().get_opts_data(
        get_futures_data_url="https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/Options/",
        app_path="/Applications/Google\ Chrome.app"
    )
    # # 一般交易行情
    # FinanceCrawler().get_opts_data(
    #     get_futures_data_url="https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/Options/",
    #     app_path="/Applications/Google\ Chrome.app"
    # )

    # desLogPhysicalPrice = 16101 + 16
    # exercisePrice = 16000
    # noRiskRate = 1.5
    # cashStockRate = 0
    # dayType = "Period"
    # period = 23.5
    # dayYear = "DAY"
    # callPut = "call"
    # premium = 320
    # opt_n = 17
    # opt_iv = FuturesExchangeTW.get_opt_IV(
    #     desLogPhysicalPrice=desLogPhysicalPrice,
    #     exercisePrice=exercisePrice,
    #     noRiskRate=noRiskRate,
    #     cashStockRate=cashStockRate,
    #     dayType=dayType,
    #     period=period,
    #     dayYear=dayYear,
    #     callPut=callPut,
    #     premium=premium
    # )
    # print(f"opt_iv: {opt_iv['call']['OptImpliedPrice']}")
    # delta = FuturesExchangeTW.get_opt_delta(
    #     desLogPhysicalPrice=desLogPhysicalPrice,
    #     exercisePrice=exercisePrice,
    #     actionRate=opt_iv['call']['OptImpliedPrice'],
    #     noRiskRate=noRiskRate,
    #     cashStockRate=cashStockRate,
    #     dayType=dayType,
    #     period=period,
    #     dayYear=dayYear,
    #     callPut=callPut,
    # )
    # print(f"delta: {delta*opt_n}")
    #
    # theta = FuturesExchangeTW.get_opt_theta(
    #     desLogPhysicalPrice=desLogPhysicalPrice,
    #     exercisePrice=exercisePrice,
    #     actionRate=opt_iv['call']['OptImpliedPrice'],
    #     noRiskRate=noRiskRate,
    #     cashStockRate=cashStockRate,
    #     dayType=dayType,
    #     period=period,
    #     dayYear=dayYear,
    #     callPut=callPut,
    # )
    # print(f"theta: {theta*opt_n}")

