#!/usr/bin/env python3
"""
This module defines a function to fetch and cache web pages, and
track the number of times a URL is accessed.
"""

import redis
import requests
from typing import Callable

# Initialize Redis client
r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL, caches it for 10 seconds,
    and tracks the number of times the URL has been accessed.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the URL.
    """
    # Key to track the number of accesses
    count_key = f"count:{url}"

    # Increment the URL access count
    r.incr(count_key)

    # Check if the content is already cached in Redis
    cached_page = r.get(url)
    if cached_page:
        return cached_page.decode('utf-8')

    # If not cached, fetch the page content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with an expiration of 10 seconds
    r.setex(url, 10, html_content)

    return html_content


# Bonus: Implementing with decorators

def track_access(method: Callable) -> Callable:
    """
    Decorator to track the number of times a URL is accessed.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method with access tracking.
    """
    def wrapper(url: str, *args, **kwargs):
        # Key to track access count
        count_key = f"count:{url}"
        # Increment the URL access count
        r.incr(count_key)
        return method(url, *args, **kwargs)
    return wrapper


def cache_with_expiry(expiry: int) -> Callable:
    """
    Decorator to cache the result of a function for a certain amount of time.
    Args:
        expiry (int): Time in seconds for the cache expiration.
    Returns:
        Callable: The wrapped method with caching.
    """
    def decorator(method: Callable) -> Callable:
        def wrapper(url: str, *args, **kwargs):
            # Check if the content is already cached
            cached_page = r.get(url)
            if cached_page:
                return cached_page.decode('utf-8')

            # If not cached, call the original method and cache the result
            result = method(url, *args, **kwargs)
            r.setex(url, expiry, result)
            return result
        return wrapper
    return decorator


@track_access
@cache_with_expiry(10)
def get_page_with_decorators(url: str) -> str:
    """
    Fetches the HTML content of a URL, caches it for 10 seconds, and
    tracks the number of times the URL has been accessed.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


# Testing the functionality
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"

    # Test without decorators
    print(get_page(test_url))
    print(f"URL accessed {r.get(f'count:{test_url}').decode('utf-8')} times.")

    # Test with decorators
    print(get_page_with_decorators(test_url))
    print(f"URL accessed {r.get(f'count:{test_url}').decode('utf-8')} times.")
