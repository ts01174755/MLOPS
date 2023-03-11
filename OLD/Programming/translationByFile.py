import os; os.chdir('./File/MLOPS_w3')
from dotenv import load_dotenv, find_dotenv
import openai
from package.CICD.MLFlow import MLFlow, dataFlow
from OLD.FileSystem import FileSystem
from OLD.Modeling.Application.translationByChatGPT import translationByChatGPT


load_dotenv(find_dotenv('../../env/.env'))

if __name__ == '__main__':
    # 用工廠模式派生多個機器學習流程
    translationByChatGPT = MLFlow(translationByChatGPT())

    # 印出當今目錄下所有檔案
    for root, dirs, files in os.walk(os.getcwd()):
        if root.split('/')[-1] != 'Raw': continue

        for file_ in files:
            if file_.split('.')[-1] != 'txt': continue

            # 讀取檔案
            sentences = translationByChatGPT.rawdata(
                filePath = f'{root}/{file_}',
                alert = False,
                dataFlowAction = 'rawdata',
                dataFlowCommit = '資料讀取'
            )
            # 翻譯
            sentences = translationByChatGPT.preprocess(
                sentences = sentences,
                sentenceLength = 1024,
                alert = False,
                dataFlowAction = 'preprocess',
                dataFlowCommit = '每筆資料至少要1024字'
            )
            data_translate = translationByChatGPT.modelAPI(
                sentences = sentences,
                api_key = os.getenv("OPENAI_API_KEY"),
                modelObject = openai,
                modelParameter = {
                    'engine': "text-davinci-003",
                    'max_tokens': 2048,
                    'top_p': 1,
                    'stop': None,
                    'temperature': 1,
                },
                alert = True,
                dataFlowAction = 'SaveData',
                dataFlowCommit= 'CallChatGPT做翻譯'
            )

            # 儲存檔案
            dataFlow.dataflow(FileSystem.saveListToTxt, {
                'path': f"./Translate/{file_.replace('.txt', '')}_translation2.txt",
                'data': data_translate,
                'dataFlowAction': 'SaveData',
                'dataFlowCommit': 'CallChatGPT做翻譯'
            })
