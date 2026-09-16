import functools

def repeat_decor(_func=None, *, repeat=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(repeat):
                result = func(*args, **kwargs)
            return result
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


#repeat_decor_arg(repeat_decor(api_request))

#repeat_decor_arg(decorator)

@repeat_decor(repeat=2)
def api_request():
    print('api request')

#repeat_decor(api_request)
@repeat_decor
def api_request_1():
    print('api request')

api_request()
api_request_1()