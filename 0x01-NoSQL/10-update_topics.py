#!/usr/bin/env python3
"""
A Python module that changes all topics of a school
document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    a Python function that changes all
    topics of a school document based on the name
    """
    query = {"name": name}
    add_vals = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, add_vals)
