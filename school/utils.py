from django.utils.timezone import utc

from .models import HomeWork
import datetime
import pytz
utc = pytz.UTC


def CheckHomeWork():
    homeworks = HomeWork.objects.all()
    for homework in homeworks:
        if utc.localize(homework.end) < utc.localize(datetime.datetime.now()):
            homework.completed = True
            homework.save()
