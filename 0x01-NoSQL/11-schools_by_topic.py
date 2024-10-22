#!/usr/bin/env python3
"""
Module to find schools by topic in MongoDB
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.
    Args:
        mongo_collection: the pymongo collection object
        topic (str): the topic to search for
    Returns:
        A list of schools with the specified topic
    """
    return mongo_collection.find({ "topics": topic })
