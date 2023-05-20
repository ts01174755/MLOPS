from multiprocessing import Process, Pipe
from STPython_3_8_16.model.futures_exchange_tw import FinanceCrawler, FuturesExchangeTW
import json
import datetime
import time

class InvestDashboard:
    def __init__(self):
        self.finance_crawler_parent_conn, self.finance_crawler_child_conn = Pipe()
        self.finance_AH_crawler_parent_conn , self.finance_AH_crawler_child_conn = Pipe()
        self.opt_crawler_parent_conn, self.opt_crawler_child_conn = Pipe()
        self.opt_AH_crawler_parent_conn, self.opt_AH_crawler_child_conn = Pipe()
        self.finance_crawler_process = None
        self.opt_crawler_process = None

    # 取得期貨、選擇權資料
    def run_futures_crawler(self):
        finance_crawler_process = Process(
            target=FinanceCrawler.get_futures_data,
            args=(
                "https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/FuturesDomestic/",
                "/Applications/Google\ Chrome.app",
                self.finance_crawler_child_conn
            )
        )
        finance_crawler_process.start()

        opt_crawler_process = Process(
            target=FinanceCrawler.get_opts_data,
            args=(
                "https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/Options/",
                "/Applications/Google\ Chrome.app",
                self.opt_crawler_child_conn
            )
        )
        opt_crawler_process.start()

        self.finance_crawler_process = finance_crawler_process
        self.opt_crawler_process = opt_crawler_process

        return True

    # 取得盤後期貨、選擇權資料
    def run_futures_AH_crawler(self):
        finance_AH_crawler_process = Process(
            target=FinanceCrawler.get_futures_data,
            args=(
                "https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/FuturesDomestic/",
                "/Applications/Google\ Chrome.app",
                self.finance_AH_crawler_child_conn
            )
        )
        finance_AH_crawler_process.start()

        opt_AH_crawler_process = Process(
            target=FinanceCrawler.get_opts_data,
            args=(
                "https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/Options/",
                "/Applications/Google\ Chrome.app",
                self.opt_AH_crawler_child_conn
            )
        )
        opt_AH_crawler_process.start()

        self.finance_AH_crawler_process = finance_AH_crawler_process
        self.opt_AH_crawler_process = opt_AH_crawler_process

        return True

    # 關閉期貨、選擇權爬蟲
    def close_futures_crawler(self):
        if self.finance_crawler_process is not None:
            self.finance_crawler_process.terminate()
        if self.opt_crawler_process is not None:
            self.opt_crawler_process.terminate()

    # 關閉盤後期貨、選擇權爬蟲
    def close_futures_AH_crawler(self):
        if self.finance_AH_crawler_process is not None:
            self.finance_AH_crawler_process.terminate()
        if self.opt_AH_crawler_process is not None:
            self.opt_AH_crawler_process.terminate()

    # 取得期貨、選擇權資料
    def get_invest_data(self, futures_data, opt_data):
        while self.finance_crawler_parent_conn.poll():
            try:
                time_now, futures_data = self.finance_crawler_parent_conn.recv()
            except Exception as e:
                print(e)
                pass

        while self.opt_crawler_parent_conn.poll():
            try:
                time_now, opt_data = self.opt_crawler_parent_conn.recv()
            except Exception as e:
                print(e)
                pass

        return futures_data, opt_data

    # 取得盤後期貨、選擇權資料
    def get_invest_AH_data(self, futures_AH_data, opt_AH_data):
        while self.finance_AH_crawler_parent_conn.poll():
            try:
                time_now, futures_AH_data = self.finance_AH_crawler_parent_conn.recv()
            except Exception as e:
                print(e)
                pass

        while self.opt_AH_crawler_parent_conn.poll():
            try:
                time_now, opt_AH_data = self.opt_AH_crawler_parent_conn.recv()
            except Exception as e:
                print(e)
                pass

        return futures_AH_data, opt_AH_data

    # 計算期貨價格
    def compute_futures_data(self, futures_data):
        # TWII指數價格
        tw_index = None if futures_data['成交價'][0] == '--' else float(futures_data['成交價'][0].replace(',', ''))

        return tw_index

    # 計算盤後期貨價格
    def compute_futures_AH_data(self, futures_AH_data):
        # TWII指數價格_夜盤
        tw_index_ = None if futures_AH_data['參考價'][0] == '--' else float(futures_AH_data['參考價'][0].replace(',', ''))
        futures_buy_price = None if futures_AH_data['買進'][10] == '--' else float(futures_AH_data['買進'][10].replace(',', ''))
        futures_sell_price = None if futures_AH_data['賣出'][10] == '--' else float(futures_AH_data['賣出'][10].replace(',', ''))
        futures_price = None if futures_AH_data['成交價'][10] == '--' else float(futures_AH_data['成交價'][10].replace(',', ''))
        futures_delta = None if futures_AH_data['漲跌'][10] == '--' else float(futures_AH_data['漲跌'][10].replace(',', ''))
        if futures_buy_price is None or futures_sell_price is None:
            tw_index = tw_index_
        else:
            futures_delta_AH = (futures_buy_price + futures_sell_price) / 2 - futures_price + futures_delta
            tw_index = tw_index_ + futures_delta_AH

        return tw_index

    # 計算選擇權價格
    def compute_opt_data(self, opt_strike_price, opt_data):
        # 選擇權價格
        opt_target_index = 0
        for key_, val_ in opt_data['履約價'].items():
            if val_.find(str(opt_strike_price)) != -1:
                opt_target_index = key_
                break
        opt_buy_price = None if opt_data['買權_買進'][opt_target_index] == '--' else float(opt_data['買權_買進'][opt_target_index].replace(',', ''))
        opt_sell_price = None if opt_data['買權_賣出'][opt_target_index] == '--' else float(opt_data['買權_賣出'][opt_target_index].replace(',', ''))
        if opt_buy_price is None or opt_sell_price is None:
            opt_price = None
        else:
            opt_price = (opt_buy_price + opt_sell_price) / 2

        return opt_price

    # 計算盤後選擇權價格
    def compute_opt_AH_data(self, opt_strike_price, opt_AH_data):
        # 選擇權價格
        opt_target_index = 0
        for key_, val_ in opt_AH_data['履約價'].items():
            if val_.find(str(opt_strike_price)) != -1:
                opt_target_index = key_
                break
        opt_buy_price = None if opt_AH_data['買權_買進'][opt_target_index] == '--' else float(opt_AH_data['買權_買進'][opt_target_index].replace(',', ''))
        opt_sell_price = None if opt_AH_data['買權_賣出'][opt_target_index] == '--' else float(opt_AH_data['買權_賣出'][opt_target_index].replace(',', ''))
        if opt_buy_price is None or opt_sell_price is None:
            opt_price = None
        else:
            opt_price = (opt_buy_price + opt_sell_price) / 2

        return opt_price

    # 計算理論價格
    def opt_opt_theory_data(self, opt_strike_price, opt_expire_date, opt_type, tw_index, opt_price):
        # 計算期間
        opt_expire_year = int(opt_expire_date.split('/')[0])
        opt_expire_month = int(opt_expire_date.split('/')[1])
        opt_expire_day = int(opt_expire_date.split('/')[2])
        opt_expire_time = datetime.datetime(opt_expire_year, opt_expire_month, opt_expire_day, 13, 30, 0)
        period = opt_expire_time - datetime.datetime.now()
        period_days = round(period.days + period.seconds / 86400 - 10, 4)

        opt_iv = FuturesExchangeTW.get_opt_IV(
            desLogPhysicalPrice=tw_index,    # 標的物現價
            exercisePrice=opt_strike_price,            # 履約價
            noRiskRate=1.5,         # 無風險利率
            cashStockRate=0,        # 股息率
            dayType="Period",       # 期間類型
            period=period_days,     # 期間
            dayYear="DAY",          # 一年幾天
            callPut=opt_type,       # 買權(Call)或賣權(Put)
            premium=opt_price         # 選擇權市價
        )
        delta = FuturesExchangeTW.get_opt_delta(
            desLogPhysicalPrice=tw_index,
            exercisePrice=opt_strike_price,
            actionRate=opt_iv['call']['OptImpliedPrice'],
            noRiskRate=1.5,
            cashStockRate=0,
            dayType="Period",
            period=period_days,
            dayYear="DAY",
            callPut=opt_type,
        )
        theta = FuturesExchangeTW.get_opt_theta(
            desLogPhysicalPrice=tw_index,
            exercisePrice=opt_strike_price,
            actionRate=opt_iv['call']['OptImpliedPrice'],
            noRiskRate=1.5,
            cashStockRate=0,
            dayType="Period",
            period=period_days,
            dayYear="DAY",
            callPut=opt_type,
        )
        return opt_iv['call']['OptImpliedPrice'], delta, theta

