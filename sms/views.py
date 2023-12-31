from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import*
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import pagination
from django.http import Http404
from .permissions import CustomPermission
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserListSerializer

)
import pandas as pd
from .models import CustomUser
from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from django.http import HttpResponse
from .models import *
import csv
from .email import*



    # 



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    # Your view code here
    return Response(...)

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
class TokenRefreshView(TokenRefreshView):
    pass


class AuthUserRegistrationView(APIView):
    users = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
         
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            email_otp(serializer.data['email'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class VerifyOtp(APIView):
    serializer_class = VerifyAccountSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
         
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code) 
              
    
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = CustomUser.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
        
class UserDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None): 
        user = self.get_object(pk)  
        users =request.user
        if users.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
        else:
            user.delete()
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': user and 'successfully deleted',
            }

        return Response(response, status=status.HTTP_200_OK)

    
        
        
class StudentsViewSets(viewsets.ModelViewSet):
    queryset=Students.objects.all()
    serializer_class= StudentsSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

def export_to_csv_students(request):
    students= Students.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=students_export.csv'
    writer = csv.writer(response)
    writer.writerow(['name', 'roll_no', 'email', 'father_name', 'age', 'mother_name', 'date_of_birth', 'mothers_mobile_no', 'fathers_mobile_no', 'gender', 'gender', 'date_of_joining', 'class_name'])
    students_fields = students.values_list('name', 'roll_no', 'email', 'father_name', 'age', 'mother_name', 'date_of_birth', 'mothers_mobile_no', 'fathers_mobile_no', 'gender', 'gender', 'date_of_joining', 'class_name')
    for student in students_fields:
        writer.writerow(student)
    return response


class StaffViewSets(viewsets.ModelViewSet):
    def get_queryset(self):
        staff = Staff.objects.all()
        return staff
    serializer_class= StaffSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

def export_to_csv_staff(request):
    staff= Staff.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=staff_export.csv'
    writer = csv.writer(response)
    writer.writerow(['name', 'staff_id', 'email', 'mobile_no', 'alternate_mobile_no', 'gender', 'date_of_birth', 'date_of_joining', 'subjects', 'subject_details', 'class_name', 'class_details'])
    staff_fields = staff.values_list('name', 'staff_id', 'email', 'mobile_no', 'alternate_mobile_no', 'gender', 'date_of_birth', 'date_of_joining', 'subjects', 'subject_details', 'class_name', 'class_details')
    for teacher in staff_fields:
        writer.writerow(teacher)
    return response


class ClassViewSets(viewsets.ModelViewSet):
    def get_queryset(self):
        classes = Clss.objects.all()
        return classes
    serializer_class= ClssSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

def export_to_csv_class(request):
    classes= Clss.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename= class_export.csv'
    writer = csv.writer(response)
    writer.writerow(['name', 'subjects', 'subject_details'])
    class_fields = classes.values_list('name', 'subjects', 'subject_details')
    for standard in class_fields:
        writer.writerow(standard)
    return response


class SubjectViewSets(viewsets.ModelViewSet):
    def get_queryset(self):
        subjects = Subject.objects.all()
        return subjects
    serializer_class= SubjectSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

def export_to_csv_subject(request):
    subjects= Subject.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=all_export.csv'
    writer = csv.writer(response)
    writer.writerow(['subject name', 'subject code'])
    subject_fields = subjects.values_list('subject_name', 'subject_code')
    for subject in subject_fields:
        writer.writerow(subject)
    return response

class FeesViewSets(viewsets.ModelViewSet):
    def get_queryset(self):
        fees = Fees.objects.all()
        return fees
    serializer_class= FeesSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

def export_to_csv_fees(request):
    fees= Fees.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=fee_export.csv'
    writer = csv.writer(response)
    writer.writerow(['student name', 'total fee', 'fee paid', 'balance'])
    fees_fields = fees.values_list('student_name', 'total_fee', 'fee_paid', 'balance')
    for fee in fees_fields:
        writer.writerow(fee)
    return response

# print("⢠⡠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⡠⣤")
# print("⢸⢰⠉⠢⡀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣤⣀⠀⠀⠀⠀⠀ ⣠⣾⡇⣿")
# print(" ⠣⡑⢄⠈⠢⡀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⣠⣾⣿⣿⡷⠋")
# print("  ⠈⠲⡑⢄⠈⣲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⡥⠋")
# print("    ⠈⠢⣗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡹⠋")
# print("      ⠘⠿⢿⣿⣿⣿⡿⠿⠿⠿⡿⠿⠿⡏")
# print("⠀⠀⠀⠀⠀⠀⠀⢃⠘⢿⣿⡿⠃⠀⠑⠒⡗⠊⢠⡅")
# print("⠀⠀⠀⠀⠀⠀⠀⣴⢢⡀⠀⠀⢰⣦⠀⠀⠁⣠⣾⣷⡀")
# print("⠀⠀⣿⠣⡒⣤⠒⣿⣠⡎⠒⡤⠤⡤⠤⡔⢸⠢⡛⠋⠁⠀⠀⠀⢀⡰⢀⠇")
# print("⠀⠀⠛⠃⢉⠀⣩⣿⣿⢏⡐⡗⠀⡇⠐⡗⣉⣄⠈⠢⡀⢀⠀⠀⠀⠒")
# print("⠀⠀⠀⠀⣸⣿⣿⡟⡿⠳⡈⠁⠒⠓⠀⠉⡘⠢⣑⣄⣨⡿⡁")
# print("⠀⠀⣠⣾⣿⣿⡿⣏⠀⠀⠈⠂⠤⠤⠄⠊⠀⠀⢈⣾⡯⡖⣾⡦⡀")
# print("⠀⢺⣿⣿⡿⠋⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠻⣓⣨⣿⠂")
# print("⠀⠀⠙⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠈⠛⠁")







