from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from api.models import *
from django.forms import model_to_dict
from . import parser, matcher, switcher, ranker
from celery import shared_task

def index(request):
    return HttpResponse('success!\n')

def _success(stat, data):
    return JsonResponse({ 'stat': stat, **data })

def _fail(stat, error_msg):
    return JsonResponse({ 'stat': stat, 'error': error_msg })

def index(request):
    return HttpResponse("Hello World!")

def prod(request):
    query = request.GET.dict()
    asin = query['asin']
    # prod, properties, reviews = parse(asin)
    # parse.delay(asin)
    parse(asin)
    # relationships = match.keyword_match(properties, reviews, prod)
    # save_relationship(relationships, prod)
    ret = find_relationship(asin)
    return _success(200, ret)

# @shared_task
def parse(asin):
    reviews = parser.ParseReviews(asin)
    # print(reviews)
    prod_query = parser.ParseProduct(asin)
    prod, properties = save_prod(prod_query)
    saved_reviews = save_review(reviews, prod)
    # print(saved_reviews)
    ret = matcher.keyword_match(properties, saved_reviews, prod)
    # print(len(ret))
    return

def find_relationship(prod):
    ret = {}
    related_properties = Property.objects.filter(prod = prod)
    for property in related_properties:
        relationships = Relationship.objects.filter(prod = prod, related_property = property)
        ret[property.xpath] = ranker.rank(relationships)
    return ret

def save_prod(query):
    asin = query['asin']
    product_name = query['name']
    try:
        prod = Product.objects.get(pk=asin)
        properties = Property.objects.filter(prod=prod)
    except ObjectDoesNotExist:
        prod = Product.objects.create(asin=asin, title=product_name)
        prod.save()
        properties = save_property(query, prod)
    return prod, properties

def save_review(reviews, prod):
    saved_reviews = []
    for review_info in reviews:
        try:
            review = Review.objects.get(review_id = review_info['review_id'])
        except ObjectDoesNotExist:
            review = Review.objects.create(review_id = review_info['review_id'], content=review_info['review_text'], prod=prod)
            saved_reviews.append(review)
    return saved_reviews

def save_property(query, prod):
    properties = query['properties']
    saved_properties = []
    for key, value in properties.items():
        # print(switch.switch(value))
        property = Property.objects.create(xpath = key, prod = prod, text_content = switcher.switch(value), topic = value)
        property.save()
        saved_properties.append(property)
    return saved_properties

####Deprecated####
# def highlight(request):
#     query = request.GET.dict()
#     review_id = query['review']
#     related_review = Review.objects.get(pk=review_id)
#     asin = related_review.prod.asin
#     related_prod = Product.objects.get(pk=asin)
#     all_relation = Relationship.objects.filter(related_review=related_review, prod=related_prod)
#     ret_list = []
#     for relation in all_relation:
#         ret_list.append({'sentence':relation.best_sentence,
#         'property' : relation.related_property.topic,
#         'sentiment' : relation.sentiment})
#     return _success(200, {'content':ret_list})
