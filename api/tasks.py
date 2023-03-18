from celery import shared_task
from random import randint

from .models import Producer


@shared_task
def add_random_debt():
    qs = Producer.objects.all()
    for p in qs:
        p.debt = float(p.debt) + randint(5, 500)
        p.save()


@shared_task
def decrease_random_debt():
    qs = Producer.objects.all()
    for p in qs:
        p.debt = float(p.debt) - randint(100, 10000)
        if float(p.debt) < 0:
            p.debt = 0.0
        p.save()
