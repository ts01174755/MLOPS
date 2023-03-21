import os; import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.MongoDBCtrl import MongoDBCtrl
from DE_MongoDB.package.GoogleFormApi import GoogleFormApi
from dotenv import load_dotenv, find_dotenv
import time

if __name__ == '__main__':
    load_dotenv(find_dotenv('env/.env'))
    # COLLECTION = 'tempdb' # 這邊是為了測試，所以先存入 tempdb，之後再改成正式的資料庫
    COLLECTION = 'google_form' # 這邊是正式的資料庫
    FORMID = '1sqxcABwDaVFyGD1cTo0-O0BoJIGWJccioaXGkxKMZv8'
    import subprocess
    subprocess.run('pwd', shell=True)
    # 取得 google service api
    googleFormApi = MLFlow(GoogleFormApi())
    service = googleFormApi.googleServiceApi(
        TOKEN='env/token.json',
        CLIENT_SECRET_FILE='env/client_secret.json',
        SCOPES="https://www.googleapis.com/auth/forms.responses.readonly",
        DISCOVERY_DOC="https://forms.googleapis.com/$discovery/rest?version=v1",
    )

    # 取得 google form list
    result = googleFormApi.googleServiceFormList(
        service=service,
        FORMID=FORMID
    )

    # 將結果寫入 mongodb
    googleFormApi.mongodb_insert_document(
        mongoDBCtrl=MongoDBCtrl(
            user_name=os.getenv('MongoDB_USER'),
            user_password=os.getenv('MongoDB_PASSWORD'),
            host=os.getenv('MongoDB_HOST'),
            port=int(os.getenv('MongoDB_PORT')),
            database_name='originaldb'
        ),
        collection=COLLECTION,
        document={
            "FORMID": FORMID,
            "dt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 60 * 60)),
            "crawlerResText": result
        }
    )