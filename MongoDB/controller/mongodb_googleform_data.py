from MongoDB.model.google_form_api import GoogleFormApi
from src.my_model.mongodb import MongoDB


class GoogleFormData:
    def __init__(self):
        pass

    def get_googleformdata_to_mongodb(
        self,
        TOKEN,
        CLIENT_SECRET_FILE,
        SCOPES,
        DISCOVERY_DOC,
        MONGODB_INFO,
        COLLECTION,
        FORMID,
        DATATIME,
    ):
        google_form_api = GoogleFormApi()

        # 取得 google service api
        service = google_form_api.googleServiceApi(
            TOKEN=TOKEN,
            CLIENT_SECRET_FILE=CLIENT_SECRET_FILE,
            SCOPES=SCOPES,
            DISCOVERY_DOC=DISCOVERY_DOC,
        )

        # 取得 google form list
        result = google_form_api.googleServiceFormList(service=service, FORMID=FORMID)

        # 將結果寫入 mongodb
        google_form_api.mongodb_insert_document(
            mongoDBCtrl=MongoDB(
                user_name=MONGODB_INFO["MONGODB_USER"],
                user_password=MONGODB_INFO["MONGODB_PASSWORD"],
                host=MONGODB_INFO["MONGODB_HOST"],
                port=MONGODB_INFO["MONGODB_PORT"],
                database_name=MONGODB_INFO["MONGODB_DATABASE"],
            ),
            collection=COLLECTION,
            document={"FORMID": FORMID, "dt": DATATIME, "crawlerResText": result},
        )
        return "success"


if __name__ == "__main__":
    pass
