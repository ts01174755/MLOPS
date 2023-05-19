import sys
import time
import os
import subprocess
import env_config
from STPython_3_8_16.model.futures_exchange_tw import FinanceCrawler, FuturesExchangeTW
from src.model.cicd import CICD
from multiprocessing import Process, Pipe

# ---------------------- STEP - params -----------------------
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
RUN = "local"

MONGODB = env_config.MONGODB_DOCKER if RUN.find('docker') != -1 else env_config.MONGODB_LOCAL  # mongodb連線資訊
POSTGRESDB = env_config.POSTGRESDB_DOCKER if RUN.find('docker') != -1 else env_config.POSTGRESDB_LOCAL  # postgres連線資訊
PROJECT_PATH = env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH  # 存放資料的位置
FILE_PATH = env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_FILE_PATH  # 存放資料的位置
DOWNLOAD_PATH = env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_DOWNLOAD_PATH  # 存放資料的位置
LOG_PATH = f"{env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH}/server_st_log.log" if RUN.find('docker') != -1 else f"{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/server_st_log.log"  # 執行的程式

# --------------------- docker env_params ---------------------
# 執行環境 - 基本上不需要動
if RUN == "docker":
    cicd = CICD(
        local_path=env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH,
        docker_path=env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH,
        container_name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
        container_interpreter=env_config.CONTAINER_PYTHON_3_8_18_INTERPRETER,
        gitHub_url=env_config.GITHUB_URL,
        folder_ignore_list=["__pycache__", ".git", ".idea", "venv", "OLD"]
    )
    cicd.ci_run()
    cicd.cd_run(
        py_name=f"{env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH}/automation_futureTW_crawler.py",
        py_params="docker_local",
        detach=False
    )


if __name__ == "__main__":
    if RUN.find('local') != -1:
        # logfile = open("output.txt", "w")
        # 创建管道
        finance_crawler_parent_conn, finance_crawler_child_conn = Pipe()
        finance_AH_crawler_parent_conn, finance_AH_crawler_child_conn = Pipe()
        opt_crawler_parent_conn, opt_crawler_child_conn = Pipe()
        opt_AH_crawler_parent_conn, opt_AH_crawler_child_conn = Pipe()

        # 启动爬虫进程
        finance_crawler_process = Process(
            target=FinanceCrawler.get_futures_data,
            args=(
                "https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/FuturesDomestic/",
                "/Applications/Google\ Chrome.app",
                finance_crawler_child_conn
            )
        )
        finance_crawler_process.start()

        # 启动爬虫进程
        finance_AH_crawler_process = Process(
            target=FinanceCrawler.get_futures_data,
            args=(
                "https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/FuturesDomestic/",
                "/Applications/Google\ Chrome.app",
                finance_AH_crawler_child_conn
            )
        )
        finance_AH_crawler_process.start()

        # 启动爬虫进程
        opt_crawler_process = Process(
            target=FinanceCrawler.get_opts_data,
            args=(
                "https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/Options/",
                "/Applications/Google\ Chrome.app",
                opt_crawler_child_conn
            )
        )
        opt_crawler_process.start()

        # 启动爬虫进程
        opt_AH_crawler_process = Process(
            target=FinanceCrawler.get_opts_data,
            args=(
                "https://mis.taifex.com.tw/futures/AfterHoursSession/EquityIndices/Options/",
                "/Applications/Google\ Chrome.app",
                opt_AH_crawler_child_conn
            )
        )
        opt_AH_crawler_process.start()

        # 在主进程中接收数据
        tw_index = None
        tw_index_AH = None
        futures_delta_AH = None
        opt_price = None
        opt_price_AH = None
        exercisePrice = 16400
        opt_n = 23
        period = 23
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        while True:
            time.sleep(10)
            while finance_crawler_parent_conn.poll():
                try:
                    time_now, tw_index_data = finance_crawler_parent_conn.recv()
                    tw_index = None if tw_index_data['成交價'][0] == '--' else float(tw_index_data['成交價'][0].replace(',', ''))
                except Exception as e:
                    print(e)
                    pass

            while finance_AH_crawler_parent_conn.poll():
                try:
                    time_now, futures_data = finance_AH_crawler_parent_conn.recv()
                    tw_index_AH_ = None if futures_data['參考價'][0] == '--' else float(futures_data['參考價'][0].replace(',', ''))
                    futures_buy_price = None if futures_data['買進'][10] == '--' else float(futures_data['買進'][10].replace(',', ''))
                    futures_sell_price = None if futures_data['賣出'][10] == '--' else float(futures_data['賣出'][10].replace(',', ''))
                    futures_price = None if futures_data['成交價'][10] == '--' else float(futures_data['成交價'][10].replace(',', ''))
                    futures_delta = None if futures_data['漲跌'][10] == '--' else float(futures_data['漲跌'][10].replace(',', ''))
                    if futures_buy_price is None or futures_sell_price is None:
                        futures_delta_AH = None
                        tw_index_AH = tw_index_AH_
                    else:
                        futures_delta_AH = (futures_buy_price + futures_sell_price) / 2 - futures_price + futures_delta
                        tw_index_AH = tw_index_AH_ + futures_delta_AH
                except Exception as e:
                    print(e)
                    pass

            while opt_crawler_parent_conn.poll():
                try:
                    time_now, opt_data = opt_crawler_parent_conn.recv()
                    opt_target_index = 0
                    for key_, val_ in opt_data['履約價'].items():
                        if val_.find(str(exercisePrice)) != -1:
                            opt_target_index = key_
                            break
                    opt_buy_price = None if opt_data['買權_買進'][opt_target_index] == '--' else float(opt_data['買權_買進'][opt_target_index].replace(',', ''))
                    opt_sell_price = None if opt_data['買權_賣出'][opt_target_index] == '--' else float(opt_data['買權_賣出'][opt_target_index].replace(',', ''))
                    if opt_buy_price is None or opt_sell_price is None:
                        opt_price = None
                    else:
                        opt_price = (opt_buy_price + opt_sell_price) / 2
                except Exception as e:
                    print(e)
                    pass

            while opt_AH_crawler_parent_conn.poll():
                try:
                    time_now, opt_data = opt_AH_crawler_parent_conn.recv()
                    opt_target_index = 0
                    for key_, val_ in opt_data['履約價'].items():
                        if val_.find(str(exercisePrice)) != -1:
                            opt_target_index = key_
                            break
                    opt_buy_price = None if opt_data['買權_買進'][opt_target_index] == '--' else float(opt_data['買權_買進'][opt_target_index].replace(',', ''))
                    opt_sell_price = None if opt_data['買權_賣出'][opt_target_index] == '--' else float(opt_data['買權_賣出'][opt_target_index].replace(',', ''))
                    if opt_buy_price is None or opt_sell_price is None:
                        opt_price_AH = None
                    else:
                        opt_price_AH = (opt_buy_price + opt_sell_price) / 2
                except Exception as e:
                    print(e)
                    pass

            if 525 <= time.localtime().tm_hour * 60 + time.localtime().tm_min <= 825:
                if tw_index and opt_price is not None:
                    desLogPhysicalPrice = tw_index
                    premium = opt_price
                else:
                    continue
            elif 900 <= time.localtime().tm_hour * 60 + time.localtime().tm_min:
                if tw_index_AH and opt_price_AH is not None:
                    desLogPhysicalPrice = tw_index_AH
                    premium = opt_price_AH
                else:
                    continue
            elif time.localtime().tm_hour * 60 + time.localtime().tm_min <= 240:
                if tw_index_AH and opt_price_AH is not None:
                    desLogPhysicalPrice = tw_index_AH
                    premium = opt_price_AH
                else:
                    continue
            else:
                continue

            noRiskRate = 1.5
            cashStockRate = 0
            dayType = "Period"
            dayYear = "DAY"
            callPut = "call"
            opt_iv = FuturesExchangeTW.get_opt_IV(
                desLogPhysicalPrice=desLogPhysicalPrice,
                exercisePrice=exercisePrice,
                noRiskRate=noRiskRate,
                cashStockRate=cashStockRate,
                dayType=dayType,
                period=period,
                dayYear=dayYear,
                callPut=callPut,
                premium=premium
            )
            delta = FuturesExchangeTW.get_opt_delta(
                desLogPhysicalPrice=desLogPhysicalPrice,
                exercisePrice=exercisePrice,
                actionRate=opt_iv['call']['OptImpliedPrice'],
                noRiskRate=noRiskRate,
                cashStockRate=cashStockRate,
                dayType=dayType,
                period=period,
                dayYear=dayYear,
                callPut=callPut,
            )

            theta = FuturesExchangeTW.get_opt_theta(
                desLogPhysicalPrice=desLogPhysicalPrice,
                exercisePrice=exercisePrice,
                actionRate=opt_iv['call']['OptImpliedPrice'],
                noRiskRate=noRiskRate,
                cashStockRate=cashStockRate,
                dayType=dayType,
                period=period,
                dayYear=dayYear,
                callPut=callPut,
            )
            # logfile.write(f"tw_index_price: {tw_index_price}\n")
            # logfile.write(f"futures_price_end: {futures_price_end}\n")
            # logfile.write(f"futures_price: {futures_price}\n")
            # logfile.write(f"opt_price: {opt_price}\n")
            # logfile.write(f"opt_iv: {opt_iv['call']['OptImpliedPrice']}\n")
            # logfile.write(f"delta: {delta*opt_n}\n")
            # logfile.write(f"theta: {theta*opt_n}\n")
            # logfile.write("##################################################\n")
            # logfile.flush()

            print()
            print("##################################################")
            print(f"time_now: {time_now}")
            print(f"tw_index_price: {desLogPhysicalPrice}")
            print(f"opt_price: {premium}")
            print(f"opt_iv: {opt_iv['call']['OptImpliedPrice']}")
            print(f"delta: {delta*opt_n}")
            print(f"theta: {theta*opt_n}")

        finance_crawler_process.join()
        finance_AH_crawler_process.join()
        opt_crawler_process.join()
        opt_AH_crawler_process.join()