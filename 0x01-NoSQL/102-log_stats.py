#!/usr/bin/env python3
"""
Module to provide statistics about Nginx logs stored in MongoDB, including top 10 IPs
"""

from pymongo import MongoClient

def log_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB, including top 10 IPs.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    # Get total number of logs
    total_logs = collection.count_documents({})
    print(f'{total_logs} logs')

    # Get count for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_counts}")

    # Get count of GET requests to /status path
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Get top 10 most present IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print top 10 IPs
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
