from threading import Thread


def process_async(function):

    def wrapper(*args, **kwargs):
        Thread(target=function, kwargs=kwargs).start()
        
    return wrapper