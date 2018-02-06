from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ObjectDoesNotExist

from celery import shared_task, current_task
from celery.result import AsyncResult

from api.models import *
from . import parser, matcher

import time

# async crawler; basically a rewrite of parser.ParseReview
@shared_task
def parse_async(asin):
    # set the state != "PENDING", to notify that the task has started
    current_task.update_state(state="PROGRESS", meta={"page": 0})

    # celery only accepts json serializable objects as parameters
    # so we cannot pass "prod", "properties" directly
    # instead, we have to query the database again for these objects
    prod = Product.objects.get(pk=asin)
    properties = list(Property.objects.filter(prod=prod))

    pc = 0
    while True:
        # retrying is repeating 5 times? believe there's a better way
        for i in range(5):
            try:
                review_page = parser.ReviewURL(asin, pc)
                rp = parser.request_parser(review_page)
                reviews, count = parser.parse_review_list(rp)

                if count == 0: return

                saved_reviews = save_review(reviews, prod, pc)
                matcher.keyword_match(properties, saved_reviews, prod)
                break

            except ValueError:
                print("Retrying to get the correct response")

        pc += 1
        # update task state to reflect the increment in page count
        # "meta" can be accessed in main process as "AsyncResult.info"
        # which is not pointed out clearly in celery documentation
        current_task.update_state(state="PROGRESS", meta={"page": pc})

# private implementation, only used to save reviews in db
def save_review(reviews, prod, page_count):
    saved_reviews = []
    for review_info in reviews:
        try:
            Review.objects.get(review_id=review_info['review_id'])
        except ObjectDoesNotExist:
            review = Review.objects.create(
                review_id=review_info['review_id'],
                content=review_info['review_text'],
                prod=prod,
                page=page_count,
            )
            saved_reviews.append(review)
    return saved_reviews
