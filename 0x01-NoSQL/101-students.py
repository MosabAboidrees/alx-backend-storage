#!/usr/bin/env python3
"""
Module to get all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.
    Args:
        mongo_collection: the pymongo collection object
    Returns:
        A list of students sorted by their average score.
        Each student document includes the field 'averageScore'.
    """
    # Aggregation pipeline to calculate average score and sort
    pipeline = [
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]
    
    # Execute the pipeline and return the results
    return list(mongo_collection.aggregate(pipeline))
