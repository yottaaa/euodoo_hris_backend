from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import secrets

class QRcode(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, default=secrets.token_hex(16))
    date_created = models.DateTimeField(null=True,blank=True,default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.code

class AttendanceLog(models.Model):
    ATTEND_STATUS = [
        ('TIMEIN', 'time in'),
        ('TIMEOUT', 'time out'),
    ]
    employee = models.ForeignKey(User, related_name='user_attendance', on_delete=models.CASCADE)
    code = models.ForeignKey(QRcode, related_name='code_attendance', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTEND_STATUS, default='TIMEIN')
    date_created = models.DateTimeField(null=True,blank=True,default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.employee.username} ({self.status})'