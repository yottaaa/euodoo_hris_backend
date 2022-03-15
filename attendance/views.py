from os import stat
from urllib import response
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from datetime import date, datetime
from django.http import Http404, HttpResponse
from django.conf import settings
import os

from django.contrib.auth.models import User

from .serializers import AttendanceLogSerializer, QRcodeSerializer, EmployeeSerializer, AttendanceCalculateSerializer
from .models import AttendanceLog, QRcode
# Create your views here.

class AttendanceLogList(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def get_all(self, request, format=None):
        try:
            queryset = AttendanceLog.objects.all()
            serializer = AttendanceLogSerializer(queryset, many=True)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def get_users(self, request, format=None):
        try: 
            users = User.objects.all()
            serializer = EmployeeSerializer(users, many=True)
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def get_by_user(self, request, format=None):
        try:
            queryset = AttendanceLog.objects.filter(employee=request.user)
            serializer = AttendanceLogSerializer(queryset, many=True)
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def get_by_today(self, request, format=None):
        try:
            queryset = AttendanceLog.objects.filter(date_created__contains=date.today())
            serializer = AttendanceLogSerializer(queryset, many=True)
        except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def generate_qr(self, request, format=None):
        try:
            code, created = QRcode.objects.get_or_create(date_created__contains=date.today())
            serializer = QRcodeSerializer(code)
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def create(self, request, format=None):
        try:
            _status = {
                'timein': AttendanceLog.ATTEND_STATUS[0][0],
                'timeout': AttendanceLog.ATTEND_STATUS[1][0],
            }

            _code= QRcode.objects.get(code=request.data['code'])

            _attend = AttendanceLog.objects.create(
                employee=request.user,
                code=_code,
                status=_status[request.data['status']],
            )

            serializer = AttendanceLogSerializer(_attend)
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

class AttendanceLogDetail(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def get_status(self, request, format=None):
        try:
            latest_status = AttendanceLog.objects.latest('id')
        except AttendanceLog.DoesNotExist:
            return Response({'latest_status': 'TIMEOUT'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response({'latest_status': latest_status.status, 'datetime': latest_status.date_created})

    def filter_by_user_date(self, request, format=None):
        try:
            start_date = datetime.strptime(request.data['date_range'][0], '%Y-%m-%d')
            end_date = datetime.strptime(request.data['date_range'][1], '%Y-%m-%d')
            _user = User.objects.get(username=request.data['employee'])
            queryset = AttendanceLog.objects.filter(
                employee=_user,
                date_created__date__range=(start_date,end_date)
            )
            serializer = AttendanceCalculateSerializer(queryset, many=True)
        except User.DoesNotExist:
            return Response({'detail':'Employee does not exist!'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

def downloadAPK(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'app', 'euodoo_attendance.apk')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/apk")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        raise Http404