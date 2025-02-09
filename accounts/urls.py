from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# forget password


