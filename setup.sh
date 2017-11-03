#!/bin/bash

cd amazon_review
sudo rabbitmq-server
source activate amazon
python amazon_review/manage.py runserver &
celery -A amazon_review worker -l info &
./ngork http 8000 &
