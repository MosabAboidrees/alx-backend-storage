#!/usr/bin/env python3
"""
Module to insert a new document in a MongoDB collection
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.
    Args:
        mongo_collection: the pymongo collection object
        **kwargs: keyword arguments for the document to be inserted
    Returns:
        The _id of the new document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
