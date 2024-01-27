#!/usr/bin/env python3
"""Module for the redist task"""
from functools import wraps
import redis
from typing import Callable, Optional, Union
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """
    count the numbber of times the methods of 
    Cache class were called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        a wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A method for storing the history of inputs and
    outputs for a particular function
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wrap the decorated function and return the wrapper'''
        inputs = str(args)
        self._redis.rpush(key + ":inputs", inputs)
        outputs = str(method(self, *args, **kwargs))
        self._redis.rpush(key + ":outputs", outputs)
        return outputs
    return wrapper


def replay(method: Callable):
    """
    a method that shows the history of calls 
    of a particular function.
    """
    cache = redis.Redis()
    method_name = method.__qualname__
    call = cache.get(method_name).decode("utf-8")
    print(f"{method_name} was called {call} times:")
    inputs = cache.lrange(f"{method_name}:inputs", 0, -1)
    outputs = cache.lrange(f"{method_name}:outputs", 0, -1)
    for inpt, output in zip(inputs, outputs):
        inpt = inpt.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{method_name}(*{inpt}) -> {output}")


class Cache:
    """
    A class for redis cache
    """

    def __init__(self):
        """
        an init method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stored data in cache
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        get the data from cache
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        parametrize Cache.get with the correct conversion function:
        get a string from cache
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        parametrize Cache.get with the correct conversion function:
        get an int from cache
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
