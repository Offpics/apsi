import json

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    price_per_hour = models.PositiveIntegerField(null=True)

    # Dates in format '[("m-Y", "m-Y"), ("m-Y", "m-Y")]'
    dates = models.TextField(default="[]")

    def set_dates(self, dates):
        self.dates = json.dumps(dates)

    def get_dates(self):
        return json.loads(self.dates)
