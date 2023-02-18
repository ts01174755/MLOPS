# __call__方法參考文獻：
# 如果物件不是函數，可以轉為函數，並且可以傳入參數
# http://c.biancheng.net/view/2380.html
# https://blog.csdn.net/Yaokai_AssultMaster/article/details/70256621

# __getattr__方法參考文獻：
# https://blog.csdn.net/wangyiyan315/article/details/14229981
# https://cloud.tencent.com/developer/article/1195919

# 設計模式：責任鍊模式範例
class MLFlow:
    def __init__(self, nextMLFlow=None):
        self.nextMLFlow = nextMLFlow

    def rawdata(self, flowParameters):
        if self.nextMLFlow is None:
            return None
        return self.nextMLFlow.rawdata(flowParameters)

    def preprocess(self, flowParameters):
        if self.nextMLFlow is None:
            return None
        return self.nextMLFlow.preprocess(flowParameters)

    def modelAPI(self, flowParameters):
        if self.nextMLFlow is None:
            return None
        return self.nextMLFlow.modelAPI(flowParameters)

    def dataflow(self, dataflow, flowParameters):
        if self.nextMLFlow is None:
            return None
        return self.nextMLFlow.dataflow(dataflow, flowParameters)

# 設計模式：把多個function包成一個責任鍊
class MLFlow:
    def __init__(self, flow):
        self.flow = flow

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            # 印出當前的機器學習流程
            print(f'當前的機器學習流程：{self.flow.__class__.__name__}')
            # 印出當前的機器學習流程的function
            print(f'當前的機器學習流程的function：{name}')
            # 印出當前的機器學習流程的參數
            print(f'當前的機器學習流程的參數：{args}')
            # 印出當前的機器學習流程的參數
            print(f'當前的機器學習流程的參數：{kwargs}')

            # 執行當前的機器學習流程的function
            data = getattr(self.flow, name)(*args, **kwargs)
            # 印出當前的機器學習流程的function的回傳值
            print(f'當前的機器學習流程的function的回傳值：{data}')

            # 印出下一個機器學習流程
            print(f'下一個機器學習流程：{self.flow.__class__.__name__}')
            # 印出下一個機器學習流程的function
            print(f'下一個機器學習流程的function：{name}')
            # 印出下一個機器學習流程的參數
            print(f'下一個機器學習流程的參數：{args}')
            # 印出下一個
            print(f'下一個機器學習流程的參數：{kwargs}')

            # 執行下一個機器學習流程的function
            data = getattr(self.flow, name)(*args, **kwargs)
            # 印出下一個機器學習流程的function的回傳值
            print(f'下一個機器學習流程的function的回傳值：{data}')
            return data
        return wrapper

# 用__getattr__動態把多個function註冊到一個物件中
class MLFlow:
    def __init__(self, model):
        self.model = model
        self.dataflow = None

    def __getattr__(self, name):
        def func(*args, **kwargs):
            return getattr(self.model, name)(*args, **kwargs)
        return func

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

if __name__ == '__main__':
    # 給個調用MLFlow中物件的範例
    # 用工廠模式派生多個機器學習流程
    NoteByFile = MLFlow(NoteByFile())
    NoteByFile.dataflow = NoteByFile.rawdata
    NoteByFile.dataflow = NoteByFile.preprocess
    NoteByFile.dataflow = NoteByFile.modelAPI
    NoteByFile.dataflow = NoteByFile.postprocess
    NoteByFile.dataflow = NoteByFile.save
    NoteByFile.dataflow = NoteByFile.output

