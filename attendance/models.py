from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

class QRcode(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.date_created = timezone.now()
        super(QRcode, self).save(*args,**kwargs)
