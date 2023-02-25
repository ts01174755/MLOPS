class FileSystem(object):
    def __init__(self):
        pass

    @classmethod
    def saveListToTxt(cls, flowParameters):
        path = flowParameters['path']
        data = flowParameters['data']
        # 複寫檔案
        with open(path, 'w') as f:
            for item in data:
                f.write("%s " % item)

        detectStr = 'detectStr'
        obj = None
        objLog = 'None'
        commitLog = 'saveListToTxt'
        return detectStr, obj, objLog, commitLog