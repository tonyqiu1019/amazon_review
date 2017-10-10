from django.db import models
import datetime

class Product(models.Model):
    title = models.CharField(max_length=1024, default='')
    asin = models.CharField(max_length=1024, default='', primary_key=True)
    last_crawl_date = models.DateField(default=datetime.date.today)

class Relationship(models.Model):
    related_review = models.ForeignKey('Review', on_delete=models.CASCADE)
    related_property = models.ForeignKey('Property', on_delete = models.CASCADE)
    best_sentence = models.CharField(max_length=1023, default='')
    prod = models.ForeignKey('Product', on_delete=models.CASCADE)

class Review(models.Model):
    content = models.TextField(default='')
    prod = models.ForeignKey('Product', on_delete=models.CASCADE)
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    review_id = models.CharField(max_length=1024, primary_key=True)

class Property(models.Model):
    prod = models.ForeignKey('Product', on_delete=models.CASCADE)
    xpath = models.CharField(max_length=1024, default='')
    # related_review = models.ManyToManyField(Review)
    text_content = models.CharField(max_length=1024, default='')
