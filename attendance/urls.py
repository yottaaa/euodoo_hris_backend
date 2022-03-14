from django.urls import path
from .views import AttendanceLogList, AttendanceLogDetail

urlpatterns = [
    path('users/', AttendanceLogList.as_view({'get': 'get_users'}), name='attend-users'),
    path('all/', AttendanceLogList.as_view({'get': 'get_all'}), name='attend-all'),
    path('by_user/', AttendanceLogList.as_view({'get': 'get_by_user'}), name='attend-by-user'),
    path('today/', AttendanceLogList.as_view({'get': 'get_by_today'}), name='attend-by-today'),
    path('generate_qr/', AttendanceLogList.as_view({'get': 'generate_qr'}), name='attend-generate-qr'),
    path('create/', AttendanceLogList.as_view({'post': 'create'}), name='attend-create'),

    path('latest_status/', AttendanceLogDetail.as_view({'get': 'get_status'}), name='latest-status'),
    path('filter/', AttendanceLogDetail.as_view({'post': 'filter_by_user_date'}), name='filter-user-date'),
]