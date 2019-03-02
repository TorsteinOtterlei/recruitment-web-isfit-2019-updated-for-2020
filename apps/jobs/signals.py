from django.db.models.signals import post_save, pre_save
from django.db import models
# local
from apps.jobs.models import Date
# other apps
from accounts.models import User

def create_date(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        date = Date(user=user)
        date.save()

post_save.connect(create_date, sender=User, dispatch_uid="dates-profilecreation-signal")
