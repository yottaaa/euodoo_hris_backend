from os import stat
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from datetime import date

from .serializers import AttendanceLogSerializer, QRcodeSerializer
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
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response({'latest_status': latest_status.status, 'datetime': latest_status.date_created})