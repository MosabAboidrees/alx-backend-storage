#!/usr/bin/env python3
"""
Module to update topics of a school document in MongoDB
"""

def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.
    Args:
        mongo_collection: the pymongo collection object
        name (str): the school name to update
        topics (list of str): the list of topics to be set in the document
    Returns:
        None
    """
    mongo_collection.update_many(
        { "name": name },
        { "$set": { "topics": topics } }
    )
