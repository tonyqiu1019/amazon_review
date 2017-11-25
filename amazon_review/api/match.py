from __future__ import absolute_import, unicode_literals
from api.models import *
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from celery import shared_task

def keyword_match(properties, reviews, prod):
    # print(properties)
    # print(reviews)
    sid = SentimentIntensityAnalyzer()
    ret = []
    start_time = time.time()
    for property in properties:
        text = property.text_content;
        property_word = [" " + word.lower() + " " for word in text.split(" ")]
        for review in reviews:
            sentences = review.content.split('.')
            dct = {}
            maxCount = 0
            best_sentence = ''
            for i in range(len(sentences)):
                count = sum(1 for word in property_word if word in sentences[i].lower())
                if count > maxCount:
                    maxCount = count
                    best_sentence = sentences[i]
            if maxCount >= 5:
                ss = sid.polarity_scores(best_sentence.lower())['compound']
                ret.append({'related_property': property, 'best_sentence': best_sentence, 'related_review': review, 'sentiment': ss})
    save_relationship(ret, prod)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return ret;

def save_relationship(relationships, prod):
    for relation in relationships:
        # print(relation)
        relation['prod'] = prod
        rel = Relationship(**relation)
        rel.save()
