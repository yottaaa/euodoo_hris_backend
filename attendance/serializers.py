from dataclasses import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.contrib.auth.models import User
from .models import AttendanceLog, QRcode

class QRcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRcode
        fields = (
            'id',
            'code',
            'date_created',
        )

class AttendanceLogSerializer(serializers.ModelSerializer):
    employee = SerializerMethodField()
    class Meta:
        model = AttendanceLog
        fields = (
            'id',
            'employee',
            'status',
            'date_created',
        )

    def get_employee(self, obj):
        emp = User.objects.get(id=obj.employee.id)
        return {
            'username': emp.username,
            'first_name': emp.first_name,
            'last_name': emp.last_name,
        }
