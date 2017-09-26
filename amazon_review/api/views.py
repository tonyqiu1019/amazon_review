from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from api.models import *
from django.forms import model_to_dict
from . import parser, match

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
    prod, properties, reviews = parse(asin)
    ret = match.keyword_match(properties, reviews)
    return _success(200, ret)

def parse(asin):
    prod_info = parser.ParseReviews(asin)
    prod, related_properties = save_prod(prod_info)
    reviews = save_review(prod_info, prod)
    return prod, related_properties, reviews

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

def save_review(query, prod):
    reviews = query['reviews']
    saved_reviews = []
    for review_info in reviews:
        try:
            review = Review.objects.get(review_id = review_info['review_id'])
        except ObjectDoesNotExist:
            review = Review.objects.create(review_id = review_info['review_id'], content=review_info['review_text'], prod=prod)
        review.save()
        saved_reviews.append(review)
    return saved_reviews

def save_property(query, prod):
    properties = query['properties']
    print(properties)
    saved_properties = []
    for key, value in properties.items():
        property = Property.objects.create(xpath = key, prod = prod, text_content = value)
        property.save()
        saved_properties.append(property)
    return saved_properties
