#!/usr/bin/env python3
"""
In this task, we implement a `get_page` function that fetches and caches
the HTML content of a URL. The function tracks how many times a URL
is accessed and stores the HTML response in Redis for 10 seconds.
Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response
and test the caching functionality.
"""

import redis  # Redis is used for caching and tracking access count
import requests  # Requests is used to make HTTP requests to fetch web content
from functools import wraps  # Used for defining the decorator

# Initialize Redis client
r = redis.Redis()


def url_access_count(method):
    """Decorator to track the access count of a URL and cache the result.
    This decorator wraps the `get_page` function to:
    - Check if the HTML content for a URL is already cached in Redis.
    - If the content is cached, return it directly from Redis.
    - If not cached, fetch the content from the web, cache it with
    a 10-second expiration, and track how many times the URL is accessed.
    """
    @wraps(method)
    def wrapper(url):
        """Wrapper function to implement caching and access count tracking.
        Args:
            url (str): The URL to fetch and cache.
        Returns:
            str: The HTML content of the URL
            (either from cache or fresh request).
        """
        # Key to store the cached content of the URL in Redis
        key = "cached:" + url

        # Check if the content is already cached in Redis
        cached_value = r.get(key)
        if cached_value:
            # If cached, return the content (decoded from bytes to string)
            return cached_value.decode("utf-8")

        # If not cached, we proceed to fetch and cache the content

        # Key to store the count of how many times the URL has been accessed
        key_count = "count:" + url

        # Fetch the content from the URL using the wrapped function (get_page)
        html_content = method(url)

        # Increment the access count for this URL
        r.incr(key_count)

        # Cache the fetched content in Redis
        # with an expiration time of 10 seconds
        r.set(key, html_content, ex=10)

        # Optionally, ensure that the key expires after 10 seconds
        r.expire(key, 10)

        # Return the freshly fetched HTML content
        return html_content

    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the URL.
    """
    # Use requests to fetch the content of the URL
    results = requests.get(url)

    # Return the raw HTML content as text
    return results.text


# Test the functionality by fetching a slow page (cached for 10 seconds)
if __name__ == "__main__":
    # Fetch the page and trigger the caching mechanism
    get_page('http://slowwly.robertomurray.co.uk')
