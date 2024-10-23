#!/usr/bin/env python3
'''A module with tools for request caching and tracking'''
import redis  # Importing the Redis library for interacting with Redis
import requests  # Importing the requests library to make HTTP requests
from datetime import timedelta  # Importing timedelta to set expiration times


def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    Args:
        url (str): The URL to fetch the content from.
    Returns:
        str: The content of the requested URL.
    '''
    # Check if the URL is valid (not None or empty)
    if url is None or len(url.strip()) == 0:
        return ''
    
    # Initialize the Redis client
    redis_store = redis.Redis()
    
    # Define keys for caching the result and tracking the request count
    res_key = 'result:{}'.format(url)  # Key for caching the URL response
    req_key = 'count:{}'.format(url)   # Key for tracking the request count
    
    # Check if the result is already cached in Redis
    result = redis_store.get(res_key)
    if result is not None:
        # If the result is cached, increment the request count in Redis
        redis_store.incr(req_key)
        return result
    
    # If the result is not cached, make a request to the URL
    result = requests.get(url).content.decode('utf-8')
    
    # Cache the result with an expiration time of 10 seconds
    redis_store.setex(res_key, timedelta(seconds=10), result)
    
    return result
