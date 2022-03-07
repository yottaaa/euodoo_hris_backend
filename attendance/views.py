from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from datetime import date

from .serializers import AttendanceLogSerializer
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

    def get_by_today(self, request, format=None):
        try:
            queryset = AttendanceLog.objects.filter(date_created__contains=date.today())
            serializer = AttendanceLogSerializer(queryset, many=True)
        except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def create(self, request, format=None):
        try:
            _status = {
                'timein': AttendanceLog.ATTEND_STATUS[0][0],
                'timeout': AttendanceLog.ATTEND_STATUS[1][0],
            }

            _code, _code_created = QRcode.objects.get_or_create(
                code=request.data['code'],
            )

            AttendanceLog.objects.create(
                employee=request.user,
                code=_code,
                status=_status[request.data['status']],
            )
        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "detail": f'{request.user.username} {request.data["status"]} successfully.',
        },status=status.HTTP_201_CREATED)
