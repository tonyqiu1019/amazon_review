from __future__ import absolute_import, unicode_literals
from api.models import *
import time

from celery import shared_task

def keyword_match(properties, reviews, prod):
    ret = []
    start_time = time.time()
    for property in properties:
        text = property.text_content;
        property_word = [" " + word.lower() + " " for word in text.split(" ")]
        for review in reviews:
            sentences = review.content.lower().split('.')
            dct = {}
            for sentence in sentences:
                dct[sentence] = sum(1 for word in property_word if word in sentence)
            best_sentences = [key for key,value in dct.items() if value == max(dct.values())]
            if dct[best_sentences[0]] > len(property_word) / 2:
                ret.append({'related_property': property, 'best_sentence': best_sentences[0], 'related_review': review})
    save_relationship(ret, prod)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return ret;

def save_relationship(relationships, prod):
    for relation in relationships:
        relation['prod'] = prod
        rel = Relationship(**relation)
        rel.save()
