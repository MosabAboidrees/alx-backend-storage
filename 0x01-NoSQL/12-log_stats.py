#!/usr/bin/env python3
'''Task 12's module: Provides some stats about Nginx logs stored in MongoDB.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.
    '''
    # Total number of logs
    print('{} logs'.format(nginx_collection.count_documents({})))

    # Methods stats
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, req_count))

    # GET requests to /status
    status_checks_count = nginx_collection.count_documents({
        'method': 'GET', 'path': '/status'
    })
    print('{} status check'.format(status_checks_count))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    # Connect to the MongoDB server
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Call the function to print stats
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
