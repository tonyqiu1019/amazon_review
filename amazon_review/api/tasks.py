from __future__ import absolute_import, unicode_literals
from django.db.utils import IntegrityError

from celery import shared_task, current_task, group
from celery.result import AsyncResult, allow_join_result

from api.models import *
from . import parser, matcher

import time

# async crawler; basically a rewrite of parser.ParseReview
@shared_task
def parse_async(asin, num_workers=1):
    # set the state != "PENDING", to notify that the task has started
    current_task.update_state(state="PROGRESS", meta={"page": 1})

    pc = 1
    while True:
        gp = group(worker.s(asin, pc+w) for w in range(num_workers))
        res = gp.apply_async()

        need_break = False
        with allow_join_result():
            for cnt in res.get(timeout=10):
                if cnt == 0: need_break = True
        if need_break: break
        pc += num_workers

        # update task state to reflect the increment in page count
        # "meta" can be accessed in main process as "AsyncResult.info"
        # which is not pointed out clearly in celery documentation
        current_task.update_state(state="PROGRESS", meta={"page": pc})


@shared_task
def worker(asin, pc):
    # celery only accepts json serializable objects as parameters
    # so we cannot pass "prod", "properties" directly
    # instead, we have to query the database again for these objects
    prod = Product.objects.get(pk=asin)
    properties = list(Property.objects.filter(prod=prod))

    res_cnt = 0
    # retrying is repeating 5 times? believe there's a better way
    for i in range(5):
        try:
            review_page = parser.ReviewURL(asin, pc)
            rp = parser.request_parser(review_page)
            reviews, count = parser.parse_review_list(rp)

            print("asin: %s, page: %d, count: %d" % (asin, pc, count))
            if count > 0:
                saved_reviews = save_review(reviews, prod, pc)
                matcher.keyword_match(properties, saved_reviews, prod)
            res_cnt = count; break

        except ValueError:
            print("Retrying to get the correct response")

    return res_cnt


# private implementation, only used to save reviews in db
def save_review(reviews, prod, page_count):
    saved_reviews = []
    for review_info in reviews:
        review = None
        try:
            review = Review.objects.create(
                review_id=review_info['review_id'],
                content=review_info['review_text'],
                prod=prod,
                page=page_count,
            )
        except IntegrityError:
            print("here")
        if review is not None: saved_reviews.append(review)
    return saved_reviews
