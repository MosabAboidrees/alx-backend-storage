#!/usr/bin/env python3
"""
This module defines the Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union


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
