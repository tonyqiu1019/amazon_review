from api.models import *

def rank(relationships):
    return no_rank(relationships)

def no_rank(relationships):
    relationship_list = []
    for relationship in relationships:
        review = relationship.related_review
        relationship_list.append({relationship.best_sentence: [review.content, review.review_id, relationship.sentiment, relationship.pk]})
    return relationship_list
