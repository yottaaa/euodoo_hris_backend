from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from knox import views as knox_views
from account import views as acc_views

urlpatterns = [
    path('login/', acc_views.LoginAPI.as_view(), name='user-login'),
    path('logout/', knox_views.LogoutView.as_view(), name='user-logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='user-logoutall'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)