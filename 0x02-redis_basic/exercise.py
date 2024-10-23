#!/usr/bin/env python3
"""
This module defines the Cache class for storing data in Redis and
decorators for counting method calls and storing call history.
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method that increments the count in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method that stores input/output history in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Get the method's qualified name
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Convert input arguments to string and store them in the 'inputs' list
        self._redis.rpush(inputs_key, str(args))

        # Call the original method and get the result
        result = method(self, *args, **kwargs)

        # Store the result in the 'outputs' list
        self._redis.rpush(outputs_key, str(result))

        # Return the result of the original method
        return result

    return wrapper


class Cache:
    """
    Cache class to interact with Redis for storing and retrieving data.
    """

    def __init__(self):
        """
        Initialize the Cache class with a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis using a random key and count the number of times
        this method is called.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The generated key for retrieving the stored data.
        """
        # Generate a random key using uuid
        key = str(uuid.uuid4())
        # Store the data in Redis
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the value from Redis and apply an optional conversion function.

        Args:
            key (str): The key to retrieve the value from Redis.
            fn (Optional[Callable]): A function to apply to the retrieved value.

        Returns:
            Union[str, bytes, int, float, None]: The value from Redis after applying fn if provided,
                                                 or None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve the string value from Redis for the given key.

        Args:
            key (str): The key to retrieve the value from Redis.

        Returns:
            str: The string value from Redis.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve the integer value from Redis for the given key.

        Args:
            key (str): The key to retrieve the value from Redis.

        Returns:
            int: The integer value from Redis.
       
