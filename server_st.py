import os
import sys
import env_config
from fastapi import FastAPI
from starlette.responses import JSONResponse
import uvicorn
import logging
import json
from src.controller.logger import LoggingMiddleware
from src.model.docker_cmd import DockerCmd
import subprocess

# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8000
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# 執行環境 - 基本上不需要動
CI_PY_NAME = f'{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/CI_docker_python3_8_16_server.py'
PY_NAME = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st.py"    # 執行的程式
DEPLOY_DETACH = True
if RUN == "docker":
    # ------------------------ env_params ------------------------
    LOCAL_INTERPRETER = env_config.MLOPS_ROOT_PATH_LOCAL_INTERPRETER
    subprocess.run(f"{LOCAL_INTERPRETER} {CI_PY_NAME}", shell=True)

    CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_SERVER_NAME     # 執行環境
    ROOT_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH    # DOCKER 執行路徑
    DOCKER_INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_SERVER_INTERPRETER      # 執行的python解釋器
    DockerCmd.dockerExec(
        name=CONTAINER_NAME,
        cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {DOCKER_INTERPRETER} {PY_NAME} local"',
        detach=DEPLOY_DETACH,
        interactive=True,
        TTY=False,
    )

# --------------------- controller env params ---------------------
MONGODB = env_config.MONGODB_DOCKER  # mongodb連線資訊
# MONGODB = env_config.MONGODB_LOCAL    # mongodb連線資訊
POSTGRESDB = env_config.POSTGRESDB_DOCKER  # postgres連線資訊
# POSTGRESDB = env_config.POSTGRESDB_LOCAL  # postgres連線資訊
PROJECT_PATH = env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH  # 存放資料的位置
# PROJECT_PATH = env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH  # 存放資料的位置
FILE_PATH = env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH  # 存放資料的位置
# FILE_PATH = env_config.MLOPS_ROOT_PATH_LOCAL_FILE_PATH  # 存放資料的位置
DOWNLOAD_PATH = env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH  # 存放資料的位置
# DOWNLOAD_PATH = env_config.MLOPS_ROOT_PATH_LOCAL_DOWNLOAD_PATH  # 存放資料的位置
LOG_PATH = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st_log.log"    # 執行的程式
# LOG_PATH = f"{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/server_st_log.log"    # 執行的程式


class CustomJSONResponse(JSONResponse):

    def __init__(self, content: any, *args, **kwargs):
        super().__init__(content, *args, **kwargs)
        self.headers["Content-Type"] = "application/json; charset=utf-8"

    def render(self, content: any) -> bytes:
        return json.dumps(content, ensure_ascii=False, allow_nan=False, indent=None, separators=(",", ":")).encode("utf-8")



# ------------------------- ROUTE ----------------------------
if RUN == "local":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler()
        ]
    )

app = FastAPI()
app.add_middleware(LoggingMiddleware)


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.get("/stCloudCourse/totalCourse")
def get_total_course():
    course_code_dict = {
        "多益影片課程": '0001',
        '國一數學(一)': '0002',
    }
    return CustomJSONResponse(content=course_code_dict)


@app.get("/stCloudCourse/{courseCode}")
def get_course_by_code(courseCode: str):
    course_detail_dict = {
        "0001": {
            '第1堂課': ['閱讀題型1', 'https://drive.google.com/file/d/1DdWhCP36JvkeG5ZBRx_D8x0uE0sfsr94/view?usp=sharing'],
            '第2堂課': ['閱讀題型2', 'https://drive.google.com/file/d/1BkVezP3UqMdcKh-bXwEn8X3U7g2CxMln/view?usp=sharing'],
            '第3堂課': ['閱讀題型3', 'https://drive.google.com/file/d/1sNT2dJNtUFSBrRs8UxzCH6Gksw-9N_Cq/view?usp=sharing'],
            '第4堂課': ['閱讀題型4', 'https://drive.google.com/file/d/1bfruj3FhVI83PIhxrCWOStA9l90SxW6-/view?usp=sharing'],
            '第5堂課': ['閱讀題型5', 'https://drive.google.com/drive/folders/1-AF7G1o1T9KkkSTRpvh5aO5uUInXWdtR?usp=sharing'],
            '第6堂課': ['閱讀題型6', 'https://drive.google.com/file/d/1iQ7HhZBECwB1Z09E6aKMRJsuM8G2T9fJ/view?usp=sharing'],
            '第7堂課': ['閱讀題型7', 'https://drive.google.com/file/d/1Us54I39cEbg0f164wsuloox4hPb0TDxi/view?usp=sharing'],
            '第8堂課': ['閱讀題型8', 'https://drive.google.com/file/d/1fOPWZfySVPmsYk8ZPe1Hc1PljjYs8iik/view?usp=sharing'],
            '第9堂課': ['閱讀題型9', 'https://drive.google.com/file/d/1QwbnSAA09zr5XEF0sROMqk9-yYb51fm-/view?usp=sharing'],
            '第10堂課': ['閱讀題型10', 'https://drive.google.com/file/d/16A8IWVz1khZMuqTz9c7sSmGVwDHFGuXF/view?usp=sharing'],
            '第11堂課': ['閱讀題型11', 'https://drive.google.com/file/d/18ePHqUVO6cjd6RJz8t9B6326xHm04z--/view?usp=sharing'],
            '第12堂課': ['閱讀題型12', 'https://drive.google.com/file/d/1BqOKaN0e3kmWNJl18lSn3xUBYuMSmREL/view?usp=sharing'],
            '第13堂課': ['閱讀題型13', 'https://drive.google.com/file/d/1yEbNPHJliukMSFMkO1axXQu6ph3PXeW6/view?usp=sharing'],
            '第14堂課': ['閱讀題型14', 'https://drive.google.com/file/d/1DetM6aQiZCdIp--oPLRLqFk9G6NeKYf3/view?usp=sharing'],
            '第15堂課': ['閱讀題型15', 'https://drive.google.com/file/d/1L1byUby4nIh7i9zid3fXmnXymN7QXciL/view?usp=sharing'],
            '第16堂課': ['閱讀題型16', 'https://drive.google.com/file/d/1F8DO_R3KlJOWDwECEaW0npCIrhMoZu35/view?usp=sharing'],
            '第17堂課': ['閱讀題型17', 'https://drive.google.com/file/d/1G3zAuRyEEMoBFxe6BH2Evq6SFqrQ_KWq/view?usp=sharing'],
            '第18堂課': ['閱讀題型18', 'https://drive.google.com/file/d/1fgshMZWIfr19xuyi7ezuffgfRGijQpTk/view?usp=sharing'],
            '第19堂課': ['閱讀題型19', 'https://drive.google.com/file/d/1LgMzNGb0xfn27k5eoBGQf0NHodMHWwoQ/view?usp=sharing'],
            '第20堂課': ['閱讀題型20', 'https://drive.google.com/file/d/1ncSAO8obGS0QGxYy--sCkkWg9_1CjJ0s/view?usp=sharing'],
            '第21堂課': ['閱讀題型21', 'https://drive.google.com/file/d/1_IkmDv75l9uJsRCzDS9q0RIyIpoXWIqQ/view?usp=sharing'],
        },
        '0002': {
          '講義': {
            '110_國一數學 _講義': [
              'https://drive.google.com/file/d/1Zig_TyyhlIPRj_MSmmEb5lzJbZxMlxcY/view?usp=sharing'
            ]
          },
          '第 1 堂課': {
            '相對與相反 相對與相反': [
              'https://drive.google.com/file/d/1BWC7YzTZ4mkW0MOLHZdj6zQya0Y6aru4/view?usp=sharing'
            ]
          },
          '第 2 堂課': {
            '相對與相反 教學例題 1': [
              'https://drive.google.com/file/d/1D74zJj7V_7DTRIejkf9noChVA_VaxE98/view?usp=sharing'
            ]
          },
          '第 3 堂課': {
            '相對與相反 教學例題 2': [
              'https://drive.google.com/file/d/1mLT-iWIieRdPbOy7wnY9g1LM5PE0tF_W/view?usp=sharing'
            ]
          },
          '第 4 堂課': {
            '相對與相反 教學例題 3': [
              'https://drive.google.com/file/d/1iAoSEgrgBZCdK3BIbblIlqEuEqWkA67B/view?usp=sharing'
            ]
          },
          '第 5 堂課': {
            '正負數與 0 的介紹 正負數與 0 的介紹': [
              'https://drive.google.com/file/d/1loerxf1Uplj8Xsm6tfiSQxOoowrs-TTo/view?usp=sharing'
            ]
          },
          '第 6 堂課': {
            '正負數與 0 的介紹 教學例題 1': [
              'https://drive.google.com/file/d/1eiEyoAWaqVXTKgUQ_bYalobhT5IZyUaY/view?usp=sharing'
            ]
          },
          '第 7 堂課': {
            '正負數與 0 的介紹 教學例題 2': [
              'https://drive.google.com/file/d/1c0n8xV8mB5fbYILsBFydOUiLnLsQx-_g/view?usp=sharing'
            ]
          },
          '第 8 堂課': {
            '正負數與 0 的介紹 教學例題 3': [
              'https://drive.google.com/file/d/1-jJTzK0Wfos1sALRfCXj4N8xk7M54Di_/view?usp=sharing'
            ]
          },
          '第 9 堂課': {
            '數線 數線的畫法': [
              'https://drive.google.com/file/d/1Wwf_85Gyn9C7DKrSAgnWGZSLqidyKOmn/view?usp=sharing'
            ]
          },
          '第 10 堂課': {
            '數線 數線上的座標': [
              'https://drive.google.com/file/d/18w8r-5zNpxp4YUTXrIYQwDLAptT17m62/view?usp=sharing'
            ]
          },
          '第 11 堂課': {
            '數線 數後動動腦:數線上的正負': [
              'https://drive.google.com/file/d/1cjxX630yv8gtJsiuFKcoDZvP1pCfXC_Y/view?usp=sharing'
            ]
          },
          '第 12 堂課': {
            '數線 數線': [
              'https://drive.google.com/file/d/1U7xHwsYLUvzQmrqCVFrseWM14KK4GRwL/view?usp=sharing'
            ]
          },
          '第 13 堂課': {
            '數線 教學例題 1': [
              'https://drive.google.com/file/d/1w5yNAaEDP51VfCsV4GGskT-5HSEiSynR/view?usp=sharing'
            ]
          },
          '第 14 堂課': {
            '數線 教學例題 2': [
              'https://drive.google.com/file/d/1s0Nw1xlggFFMVKJqWL2cWlzUO_fme5-x/view?usp=sharing'
            ]
          },
          '第 15 堂課': {
            '數線 教學例題 3': [
              'https://drive.google.com/file/d/1s0Nw1xlggFFMVKJqWL2cWlzUO_fme5-x/view?usp=sharing'
            ]
          },
          '第 16 堂課': {
            '數線 教學例題 4': [
              'https://drive.google.com/file/d/1s0Nw1xlggFFMVKJqWL2cWlzUO_fme5-x/view?usp=sharing',
              'https://drive.google.com/file/d/1BXh7R4SGOeGcKkVmeWN2Z-FokR4ZjY0e/view?usp=sharing'
            ]
          },
          '第 17 堂課': {
            '數比大小 數的比較大小': [
              'https://drive.google.com/file/d/1_J65XA7mMxrAvV4Zgdz-4krnNPD8y1r9/view?usp=sharing'
            ]
          },
          '第 18 堂課': {
            '數比大小 數比大小': [
              'https://drive.google.com/file/d/1pd6lk_-1vRC9qv9qILq0hCg4SVPS56DH/view?usp=sharing'
            ]
          },
          '第 19 堂課': {
            '數比大小 教學例題 1': [
              'https://drive.google.com/file/d/1M6QOwg8d4F6VSbW3dWsguaARixGKXchk/view?usp=sharing'
            ]
          },
          '第 20 堂課': {
            '數比大小 教學例題 2': [
              'https://drive.google.com/file/d/1M6QOwg8d4F6VSbW3dWsguaARixGKXchk/view?usp=sharing'
            ]
          },
          '第 21 堂課': {
            '數比大小 教學例題 3': [
              'https://drive.google.com/file/d/1M6QOwg8d4F6VSbW3dWsguaARixGKXchk/view?usp=sharing',
              'https://drive.google.com/file/d/1Po7lz6kNktie1-tPYZCvd8S9w9UgeDtP/view?usp=sharing'
            ]
          },
          '第 22 堂課': {
            '數線上比大小 數線上比大小': [
              'https://drive.google.com/file/d/1uax8ZKvDfnGotMMkICmlcMnoRXdMiyv1/view?usp=sharing'
            ]
          },
          '第 23 堂課': {
            '數線上比大小 教學例題 1': [
              'https://drive.google.com/file/d/1z5jUBtMzS0Rtw1SNJx2OUKHy2_a5XpUT/view?usp=sharing'
            ]
          },
          '第 24 堂課': {
            '數線上比大小 教學例題 2': [
              'https://drive.google.com/file/d/1z5jUBtMzS0Rtw1SNJx2OUKHy2_a5XpUT/view?usp=sharing'
            ]
          },
          '第 25 堂課': {
            '數線上比大小 教學例題 3': [
              'https://drive.google.com/file/d/1z5jUBtMzS0Rtw1SNJx2OUKHy2_a5XpUT/view?usp=sharing',
              'https://drive.google.com/file/d/196HP_keYCbwQMHHwz75H5I49eyzTDg7C/view?usp=sharing'
            ]
          },
          '第 26 堂課': {
            '相反數 相反數': [
              'https://drive.google.com/file/d/1CpPgozBs_3_THEfBRH7Stcy_cYWVWneH/view?usp=sharing'
            ]
          },
          '第 27 堂課': {
            '相反數 相反數': [
              'https://drive.google.com/file/d/1CpPgozBs_3_THEfBRH7Stcy_cYWVWneH/view?usp=sharing'
            ]
          },
          '第 28 堂課': {
            '相反數 教學例題 1': [
              'https://drive.google.com/file/d/1iFz7IrpIytS-lu52aldm_-cRtou0FFgM/view?usp=sharing'
            ]
          },
          '第 29 堂課': {
            '相反數 教學例題 2': [
              'https://drive.google.com/file/d/1iFz7IrpIytS-lu52aldm_-cRtou0FFgM/view?usp=sharing'
            ]
          },
          '第 30 堂課': {
            '絕對值 絕對值': [
              'https://drive.google.com/file/d/15lOrOdV2yWPRFprgJ_kQkY5YgBEcaGvN/view?usp=sharing'
            ]
          },
          '第 31 堂課': {
            '絕對值 絕對值': [
              'https://drive.google.com/file/d/15lOrOdV2yWPRFprgJ_kQkY5YgBEcaGvN/view?usp=sharing'
            ]
          },
          '第 32 堂課': {
            '絕對值 教學例題 1': [
              'https://drive.google.com/file/d/1dYTNze1Wfota6yq10b_VBkjXEFXRSDNh/view?usp=sharing'
            ]
          },
          '第 33 堂課': {
            '絕對值 教學例題 2': [
              'https://drive.google.com/file/d/1dYTNze1Wfota6yq10b_VBkjXEFXRSDNh/view?usp=sharing'
            ]
          },
          '第 34 堂課': {
            '絕對值 教學例題 3': [
              'https://drive.google.com/file/d/1dYTNze1Wfota6yq10b_VBkjXEFXRSDNh/view?usp=sharing',
              'https://drive.google.com/file/d/1b9vEHfNvEeJ4LVg1dMV1Z68nwbLysrIS/view?usp=sharing'
            ]
          },
          '第 35 堂課': {
            '絕對值 教學例題 4': [
              'https://drive.google.com/file/d/1dYTNze1Wfota6yq10b_VBkjXEFXRSDNh/view?usp=sharing',
              'https://drive.google.com/file/d/1dqqugFUIlcP6rHcL4F8Vdx2BDjMuAQ4z/view?usp=sharing'
            ]
          },
          '第 36 堂課': {
            '絕對值 教學例題 5': [
              'https://drive.google.com/file/d/1dYTNze1Wfota6yq10b_VBkjXEFXRSDNh/view?usp=sharing',
              'https://drive.google.com/file/d/1oJvo3akHFm-QPOl3CnK1e_Ko45jRxWjY/view?usp=sharing'
            ]
          },
          '第 37 堂課': {
            '絕對值比大小 絕對值比大小': [
              'https://drive.google.com/file/d/1EdXnlQ5D7qvH-LxkfClSp1BMlHCdzW0h/view?usp=sharing'
            ]
          },
          '第 38 堂課': {
            '絕對值比大小 教學例題 1': [
              'https://drive.google.com/file/d/1uROHr9gMO1CeYhFoNfcx34FiwbcjufWb/view?usp=sharing'
            ]
          },
          '第 39 堂課': {
            '絕對值比大小 教學例題 2': [
              'https://drive.google.com/file/d/1uROHr9gMO1CeYhFoNfcx34FiwbcjufWb/view?usp=sharing'
            ]
          },
          '第 40 堂課': {
            '絕對值比大小 教學例題 3': [
              'https://drive.google.com/file/d/1uROHr9gMO1CeYhFoNfcx34FiwbcjufWb/view?usp=sharing',
              'https://drive.google.com/file/d/1oCZWTuXElhC0Eox_AfZ6d0uaNCGY5USt/view?usp=sharing'
            ]
          },
          '第 41 堂課': {
            '絕對值比大小 教學例題 4': [
              'https://drive.google.com/file/d/1uROHr9gMO1CeYhFoNfcx34FiwbcjufWb/view?usp=sharing',
              'https://drive.google.com/file/d/1kBdIXIG1fWqUvjqWljGKZSDCTIMTlsoV/view?usp=sharing'
            ]
          },
          '第 42 堂課': {
            '複習 超越顛峰一': [
              'https://drive.google.com/file/d/1ixMElx_wVu4utdNWoWS0H_JF7qe-8xz9/view?usp=sharing'
            ]
          },
          '第 43 堂課': {
            '複習 超越顛峰二': [
              'https://drive.google.com/file/d/1ixMElx_wVu4utdNWoWS0H_JF7qe-8xz9/view?usp=sharing'
            ]
          }
        }


    }
    return CustomJSONResponse(content=course_detail_dict[courseCode])


if __name__ == "__main__":

    if RUN == "local":
        uvicorn.run(app, host="0.0.0.0", port=DEPLOY_PORT)