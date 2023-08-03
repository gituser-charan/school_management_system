"""
URL configuration for school_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sms import views
from sms import serializers
from sms.views import*
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('subjects', views.SubjectViewSets, basename='Subject Details')
router.register('class', views.ClassViewSets, basename='Class Details')
router.register('students',  views.StudentsViewSets, basename='students Details')
router.register('staff', views.StaffViewSets, basename='Staff Details')
router.register('fees', views.FeesViewSets, basename='Fee Details')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('verify', verifyotp.as_view(), name='verify OTP'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name= 'delete users'),
    path('export/subjects', views.export_to_csv_subject, name='subjects-export-to-csv'), 
    path('export/students', views.export_to_csv_students, name='student-export-to-csv'), 
    path('export/class', views.export_to_csv_class, name='class-export-to-csv'), 
    path('export/staff', views.export_to_csv_staff, name='staff-export-to-csv'), 
    path('export/fees', views.export_to_csv_fees, name='fees-export-to-csv'),
]
