import os

from dotenv import load_dotenv, find_dotenv
import openai
from package.mlops.MLFlow import MLFlow, dataFlow
from package.mlops.FileSystem import FileSystem
from Modeling.Application.NoteByFile import NoteByFile
os.chdir('./File/MLOPS_w2')
load_dotenv(find_dotenv('../env/.env'))

'''註冊function'''
# NoteByFile = MLFlow(NoteByFile())
# NoteByFile.dataflow = lambda x: x
# NoteByFile.dataflow(x = 'test function...')

if __name__ == '__main__':
    # 用工廠模式派生多個機器學習流程
    NoteByFile = MLFlow(NoteByFile())

    # 印出當今目錄下所有檔案
    for root, dirs, files in os.walk(os.getcwd()):
        if root.split('/')[-1] != 'Translate': continue

        for file_ in files:
            if file_.split('.')[-1] != 'txt': continue
            print(f'{root}/{file_}')
            if file_ != 'subtitle (1)_translation.txt': continue

            # 讀取檔案
            sentences = NoteByFile.rawdata(
                filePath = f'{root}/{file_}',
                alert = False,
                dataFlowAction = 'rawdata',
                dataFlowCommit = '資料讀取'
            )

            # 翻譯
            sentences = NoteByFile.preprocess(
                sentences = sentences,
                sentenceLength = 256*5,
                alert = False,
                dataFlowAction = 'preprocess',
                dataFlowCommit = '控制輸入字數'
            )
            data_translate = NoteByFile.modelAPI(
                sentences = sentences,
                api_key = os.getenv("OPENAI_API_KEY"),
                modelObject = openai,
                modelParameter = {
                    'engine': "text-davinci-003",
                    'max_tokens': 256*3,
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
                'path': f"./Note/{file_.replace('.txt', '')}_Note.txt",
                'data': data_translate,
                'dataFlowAction': 'SaveData',
                'dataFlowCommit': 'CallChatGPT做翻譯'
            })
