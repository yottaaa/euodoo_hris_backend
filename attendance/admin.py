from django.contrib import admin

from .models import QRcode, AttendanceLog

# Register your models here.
admin.site.register(QRcode)
admin.site.register(AttendanceLog)