from django.urls import path
from .views import AttendanceLogList

urlpatterns = [
    path('all/', AttendanceLogList.as_view({'get': 'get_all'}), name='attend-all'),
    path('today/', AttendanceLogList.as_view({'get': 'get_by_today'}), name='attend-by-today'),
    path('create/', AttendanceLogList.as_view({'post': 'create'}), name='attend-create'),
]