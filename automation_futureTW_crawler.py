import sys
import time
import os
import subprocess
import env_config
from STPython_3_8_16.model.futures_exchange_tw import FinanceCrawler, FuturesExchangeTW
from src.model.cicd import CICD
from multiprocessing import Process, Pipe
import json
import datetime

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
    from STPython_3_8_16.controller.invest_dashboard import InvestDashboard
    if RUN.find('local') != -1:
        # 讀取資料
        with open('STPython_3_8_16/files/hold_opt_data.json', 'r') as f:
            opt_json = json.load(f)

        # 建立爬蟲物件
        invest_dashboard = InvestDashboard()

        # 建立爬蟲進程
        invest_dashboard_flag = False
        invest_dashboard_AH_flag = False
        futures_data = None
        futures_AH_data = None
        opt_data = None
        opt_AH_data = None
        while True:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            time_localtime_now = time.localtime().tm_hour * 60 + time.localtime().tm_min
            print('time_now: ', time_now, 'time_localtime_now: ', time_localtime_now)

            time.sleep(10)
            # 日盤
            if 520 <= time_localtime_now <= 830:
                # 如果爬蟲進程沒有啟動，則啟動爬蟲進程
                if not invest_dashboard_flag:
                    invest_dashboard_flag = True
                    invest_dashboard.run_futures_crawler()

                # # 關掉盤後爬蟲進程
                # if invest_dashboard_AH_flag:
                #     invest_dashboard.close_futures_AH_crawler()

                # 如果爬蟲進程已經啟動，則取得爬蟲資料
                futures_data, opt_data = invest_dashboard.get_invest_data(futures_data, opt_data)
                if futures_data is None or opt_data is None:
                    continue

                # 計算資料
                opt_theory_data = []
                for data_ in opt_json:
                    opt_expire_date = data_[0]
                    opt_strike_price = data_[1]
                    opt_type = data_[2]
                    opt_n = data_[3]

                    tw_index = invest_dashboard.compute_futures_data(futures_data)
                    opt_price = invest_dashboard.compute_opt_data(opt_strike_price, opt_data)
                    opt_iv, delta, theta = invest_dashboard.opt_opt_theory_data(opt_strike_price, opt_expire_date, opt_type, tw_index, opt_price)
                    opt_theory_data.append([
                        f"台灣加權指數:{tw_index}",
                        f"選擇權標的時間:{opt_expire_date}",
                        f"選擇權履約價格:{opt_strike_price}",
                        f"選擇權類別:{opt_type}",
                        f"選擇權現價:{opt_price}",
                        f"選擇權波動率:{opt_iv}",
                        f"選擇權Delta總計:{delta*opt_n}",
                        f"選擇權時間價值總計:{theta*opt_n}"
                    ])
                print(opt_theory_data)

            elif (900 <= time_localtime_now) or (time_localtime_now <= 240):
                # 如果爬蟲進程沒有啟動，則啟動爬蟲進程
                if not invest_dashboard_AH_flag:
                    invest_dashboard_AH_flag = True
                    invest_dashboard.run_futures_AH_crawler()

                # # 關掉盤後爬蟲進程
                # if invest_dashboard_flag:
                #     invest_dashboard.close_futures_crawler()

                # 如果爬蟲進程已經啟動，則取得爬蟲資料
                futures_AH_data, opt_AH_data = invest_dashboard.get_invest_AH_data(futures_AH_data, opt_AH_data)
                if futures_AH_data is None or opt_AH_data is None:
                    continue

                # 計算資料
                opt_theory_data = []
                for data_ in opt_json:
                    opt_expire_date = data_[0]
                    opt_strike_price = data_[1]
                    opt_type = data_[2]
                    opt_n = data_[3]

                    tw_index = invest_dashboard.compute_futures_AH_data(futures_AH_data)
                    opt_price = invest_dashboard.compute_opt_AH_data(opt_strike_price, opt_AH_data)
                    opt_iv, delta, theta = invest_dashboard.opt_opt_theory_data(opt_strike_price, opt_expire_date, opt_type, tw_index, opt_price)
                    opt_theory_data.append([
                        f"台灣加權指數:{tw_index}",
                        f"選擇權標的時間:{opt_expire_date}",
                        f"選擇權履約價格:{opt_strike_price}",
                        f"選擇權類別:{opt_type}",
                        f"選擇權現價:{opt_price}",
                        f"選擇權波動率:{opt_iv}",
                        f"選擇權Delta總計:{delta*opt_n}",
                        f"選擇權時間價值總計:{theta*opt_n}"
                    ])
                print(opt_theory_data)
