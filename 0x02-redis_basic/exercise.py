#!/usr/bin/env python3
"""
This module defines the Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis using a random key.
        
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the value from Redis and apply an optional conversion function.

        Args:
            key (str): The key to retrieve the value from Redis.
            fn (Optional[Callable]): A function to apply to the retrieved value.

        Returns:
            Union[str, bytes, int, float, None]: The value from Redis after applying fn if provided,
                                                 or None if the key does not exist.
        """
        # Retrieve the value from Redis
        value = self._redis.get(key)
        if value is None:
            return None
        # Apply the conversion function if provided
        if fn is not None:
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
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve the integer value from Redis for the given key.

        Args:
            key (str): The key to retrieve the value from Redis.

        Returns:
            int: The integer value from Redis.
        """
        return self.get(key, fn=int)
