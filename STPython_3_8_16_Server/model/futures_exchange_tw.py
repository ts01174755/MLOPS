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
    def get_call_put_price(cls, get_call_put_price_url, desLogPhysicalPrice, exercisePrice, actionRate, noRiskRate, cashStockRate, dayType, period, dayYear):
        payload = {
            "desLogPhysicalPrice": desLogPhysicalPrice,  # 標的指數現貨價格
            "exercisePrice": exercisePrice,  # 履約價格
            "actionRate": actionRate,  # 波動率
            "noRiskRate": noRiskRate,  # 無風險利率
            "cashStockRate": cashStockRate,  # 現金股利率
            "dayType": dayType,  # 存續期間选择
            "period": period,  # 存續期間（这里的例子是30天）
            "dayYear": dayYear  # 存續期間的计算单位
        }
        response = requests.post(get_call_put_price_url, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 搜尋 class 為 'table_c' 的 table 標籤
        table = soup.find('table', {'class': 'table_c'})

        # 在這個 table 中找到所有的 td 標籤
        tds = table.find_all('td')
        data = {
            tds[0].text.strip(): float(tds[2].text.strip()),
            tds[1].text.strip(): float(tds[3].text.strip())
        }
        return data

    @classmethod
    def get_opt_IV(cls, get_opt_IV_url, desLogPhysicalPrice, exercisePrice, actionRate, noRiskRate, cashStockRate, dayType, period, dayYear, callPut, premium):
        payload = {
            'desLogPhysicalPrice': desLogPhysicalPrice,
            'exercisePrice': exercisePrice,
            'noRiskRate': noRiskRate,
            'cashStockRate': cashStockRate,
            "dayType": dayType,  # 存續期間选择
            "period": period,  # 存續期間（这里的例子是30天）
            'dayYear': dayYear,
            'callPut': callPut.lower(),  # 'call' 或者 'put'
            'premium': premium,  # 將此替換為你的權利金數值
        }

        response = requests.post(get_opt_IV_url, data=payload)
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


if __name__ == "__main__":
    call_put_price1 = FuturesExchangeTW.get_call_put_price(
        get_call_put_price_url="https://www.taifex.com.tw/cht/9/calOptPrice",
        desLogPhysicalPrice="15673",
        exercisePrice="16000",
        actionRate="11.32",
        noRiskRate="1.5",
        cashStockRate="0",
        dayType="Period",
        period="24.5",
        dayYear="DAY"
    )
    print(call_put_price1)


    opt_iv = FuturesExchangeTW.get_opt_IV(
        get_opt_IV_url="https://www.taifex.com.tw/cht/9/calOptImpliedPrice",
        desLogPhysicalPrice="15673",
        exercisePrice="16000",
        actionRate="11.44",
        noRiskRate="1.5",
        cashStockRate="0",
        dayType="Period",
        period="24.5",
        dayYear="DAY",
        callPut="call",
        premium="76"
    )
    print(opt_iv)