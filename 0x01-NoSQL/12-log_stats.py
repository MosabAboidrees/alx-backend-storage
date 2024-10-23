#!/usr/bin/env python3
"""
Module to provide statistics about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def log_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

    # Get total number of logs
    n_logs = client.count_documents({})
    print(f'{n_logs} logs')

    # Get count for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    
    print('Methods:')
    for method in methods:
        method_counts = client.count_documents({"method": method})
        print(f'\tmethod {method}: {method_counts}')

    # Get count of GET requests to /status path
    status_check_count = client.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
