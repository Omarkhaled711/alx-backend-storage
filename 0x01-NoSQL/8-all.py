#!usr/bin/env python3

"""
A Python module for listing all documents in a collection
"""


def list_all(mongo_collection):
    """
    a Python function that lists all documents in a collection
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
