


from functools import wraps

import  datetime

def dec_limit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = datetime.datetime.now()
        print(start)
        result = func(*args,**kwargs)
        stop = datetime.datetime.now()
        print(stop)
        return result


    return wrapper



@dec_limit
def pri(num):
    for item in num:
        print(item)
        new_lis = []
        new_lis.append(item)
        print(new_lis)



lis = [1,2,3,4,5]
pri(lis)