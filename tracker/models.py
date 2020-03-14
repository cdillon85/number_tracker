from django.db import models

class Number(models.Model):
    value = models.IntegerField()
    count = models.IntegerField(default=1)

    def incrementCount(self, increment_amount):
        self.count += increment_amount