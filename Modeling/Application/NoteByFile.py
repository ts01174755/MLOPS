from tqdm import tqdm
from package.mlops.MLFlow import MLFlow

# 用工廠模式派生的機器學習流程
class NoteByFile(MLFlow):
    def __init__(self):
        pass
    @classmethod
    def rawdata(cls, filePath, alert, **kwargs):
        # 讀txt檔案
        with open(filePath, 'r') as f:
            data = f.readlines()
            data = ''.join(data)
            data = data.replace('\n', '')
            data = data.split('。')
            if alert: print(data)

        return data

    @classmethod
    def preprocess(cls, sentences, sentenceLength, alert, **kwargs):
        sentencesTmp = ''
        setencesALL = []
        for sentence_ in sentences:
            sentencesTmp += sentence_
            if len(sentencesTmp) < sentenceLength:
                continue
            else:
                setencesALL.append(sentencesTmp)
                sentencesTmp = ''
        setencesALL.append(sentencesTmp)
        if alert: print(setencesALL)

        return setencesALL

    @classmethod
    def modelAPI(cls, sentences, api_key, modelObject, modelParameter, alert, **kwargs):
        data = []
        skipStr = ['「', '」']
        modelObject.api_key = api_key
        for sentence_ in tqdm(sentences):
            prompt = f"幫我做大綱筆記，大綱筆記要有「題目」、「主題」和「內容」，以下是給你的資料：\n'{sentence_}'"
            while True:
                try:
                    completion = modelObject.Completion.create(
                        engine=modelParameter['engine'],
                        prompt=prompt,
                        max_tokens=modelParameter['max_tokens'],
                        top_p=modelParameter['top_p'],
                        stop=modelParameter['stop'],
                        temperature=modelParameter['temperature'],
                    )
                    # 字串處理：一次取代多個字符
                    completionStr = completion.choices[0].text
                    for skipStr_ in skipStr:
                        completionStr = completionStr.replace(skipStr_, '')
                    data.append(completionStr)
                    if alert:
                        print(completion.choices[0].text)

                    break
                except Exception as e:
                    if alert: print(e)
                    continue

        return data


