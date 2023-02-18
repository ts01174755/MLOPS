


class oopTest(object):
    def __init__(self, oop):
        self.oop = oop

    def __getattr__(self, name):
        print(f'__getattr__:{name}')
        def wrapper(*args, **kwargs):
            # # 印出當前的機器學習流程
            # print(f'當前的機器學習流程：{self.oop.__class__.__name__}')
            # # 印出當前的機器學習流程的function
            # print(f'當前的機器學習流程的function：{name}')
            # # 印出當前的機器學習流程的參數
            # print(f'當前的機器學習流程的參數：{args}')
            # # 印出當前的機器學習流程的參數
            # print(f'當前的機器學習流程的參數：{kwargs}')

            # 執行當前的機器學習流程的function
            data = getattr(self.oop, name)(*args, **kwargs)
            # # 印出當前的機器學習流程的function的回傳值
            # print(f'當前的機器學習流程的function的回傳值：{data}')
            return data
        return wrapper

    def __getattribute__(self, item):
        # 獲取item的值
        print(f'__getattribute__:{item}')
        value = object.__getattribute__(self, item)
        # 如果item是函數，則獲取他輸入的參數
        if callable(value):
            def func_(*args, **kwargs):
                print(f'__getattribute__:{item}的參數：{args}')
                print(f'__getattribute__:{item}的參數：{kwargs}')
                return value(*args, **kwargs)
            return func_
        return value

    def funcTest_(self, *args, **kwargs):
        print("funcTest_")
        print(args, kwargs)
        return args

class oopTest2(oopTest):
    def __init__(self):
        pass

    def funcTest2_(self, *args, **kwargs):
        print("do funcTest2_...")
        print(args, kwargs)
        return args

def funcTest(*args, **kwargs):
    print("funcTest")
    print(args, kwargs)
    return args

if __name__ == '__main__':
    ooptest = oopTest(oopTest2())
    ooptest.funcTest2_(a=1)
    # ooptest.dataflow = funcTest
    # ooptest.dataflow(a=1)