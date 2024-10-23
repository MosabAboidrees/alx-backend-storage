#!/usr/bin/env python3
"""
This module defines the Cache class for storing data in Redis and
decorators for counting method calls, storing call history, and retrieving it.
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
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Store inputs as a string
        self._redis.rpush(inputs_key, str(args))

        # Call the original method
        result = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(outputs_key, str(result))

        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls to a method.

    Args:
        method (Callable): The method for which to display the history.

    Returns:
        None
    """
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    # Retrieve inputs and outputs from Redis
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    # Number of calls
    call_count = len(inputs)
    print(f"{method_name} was called {call_count} times:")

    # Iterate through inputs and outputs and display them
    for input_value, output_value in zip(inputs, outputs):
        print(f"{method_name}(*{input_value.decode('utf-8')}) -> {output_value.decode('utf-8')}")


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
        """
        return self.get(key, int)
