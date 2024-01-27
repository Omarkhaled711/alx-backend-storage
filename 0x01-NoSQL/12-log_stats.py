#!/usr/bin/env python3
"""
 a Python script that provides some stats about Nginx logs stored in MongoDB:
"""
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    log_nums = nginx_collection.count_documents({})
    print(f'{log_nums} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        counted = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {counted}')

    check_status = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{check_status} status check')
