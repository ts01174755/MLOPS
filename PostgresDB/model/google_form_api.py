class GoogleFormApi:
    def __init__(self):
        pass

    def googleServiceApi(self, TOKEN, CLIENT_SECRET_FILE, SCOPES, DISCOVERY_DOC):
        from oauth2client import client, file, tools
        from httplib2 import Http
        from apiclient import discovery

        store = file.Storage(TOKEN)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            creds = tools.run_flow(flow, store)

        service = discovery.build(
            "forms",
            "v1",
            http=creds.authorize(Http()),
            discoveryServiceUrl=DISCOVERY_DOC,
            static_discovery=False,
        )
        return service

    def googleServiceFormList(self, service, FORMID):
        # Call the Forms v1 API
        result = service.forms().responses().list(formId=FORMID).execute()
        return result

    def mongodb_insert_document(self, mongoDBCtrl, collection, document):
        # 將結果寫入 mongodb
        mongoDBCtrl.insert_document(collection, document)

        return "success"
