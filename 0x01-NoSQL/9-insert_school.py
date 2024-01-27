#!/usr/bin/env python3

"""
A Python module for inserting a new document in a collection
"""


def insert_school(mongo_collection, **kwargs):
    """
    A script that Inserts a new document in a
    collection based on kwargs
    """
    return mongo_collection.insert(kwargs)
