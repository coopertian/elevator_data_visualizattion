#!/usr/bin/env python
# coding=utf8

from functools import wraps
from concurrent.futures import ThreadPoolExecutor

__author__ = 'tiantian'


# implement asnyc
class ThreadPool(object):
    def __init__(self, future, timeout):
        self.__future = future
        self.__timeout = timeout

    def __getattr__(self, name):
        result = self.__wait()
        return result.__getattribute__(name)

    @property
    def result(self):
        return self.__wait()

    def __wait(self):
        return self.__future.result(self.__timeout)


# 带参数的异步装饰器
def async(n, base_type, timeout=None):

    def decorator(f):
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError("Invalid type: %s" % type(base_type))

        @wraps(f)
        def wrapped(*args, **kwargs):
            return ThreadPool(pool.submit(f, *args, **kwargs), timeout=timeout)
        return wrapped
    return decorator


def threads(n, timeout=None):
    return async(n, ThreadPoolExecutor, timeout)
