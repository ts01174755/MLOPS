# 參考文獻：https://skylinelimit.blogspot.com/2018/04/python-args-kwargs.html

def func_(*args, **kwargs):
    print(args)
    print(kwargs)
    return args

def func_kwargs(**kwargs):
    print(kwargs)
    return kwargs

def func_args(*args):
    print(args)
    return args

if __name__ == '__main__':
    func_(1, 2, 3, a=1, b=2, c=3)
    func_args(1, 2, 3)
    func_kwargs(a=1, b=2, c=3)
