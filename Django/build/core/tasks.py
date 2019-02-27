from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.parser.run import parse_all

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def parse():
    parse_all(["ASOS"])
