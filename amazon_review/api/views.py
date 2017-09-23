from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from parser import *
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
    return _success(200, query)

def parse(asin):
    prod, reviews = ReadAsin(asin)


def save_review(query):


def save_prod(query):


def save_property(query):
