from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import*
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password',
            'role'
        )

    def create(self, validated_data):
        auth_user = CustomUser.objects.create_user(**validated_data)
        return auth_user
"""
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'role'
        )
    """
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Subject
        fields = "__all__"
    
class ClssSerializer(serializers.ModelSerializer):
    subject_details = serializers.SerializerMethodField()
    class Meta:
        model= Clss
        fields = ['id', 'name', 'subjects', 'subject_details']
    def get_subject_details(self, obj):
        subject_objects = obj.subjects.all()
        return SubjectSerializer(subject_objects, many = True).data
    
class StudentsSerializer(serializers.ModelSerializer):
    
    #class_name = serializers.SerializerMethodField(source='get_class_name')

    class Meta:
        model= Students
        fields ="__all__"


    def to_representation(self, instance):
        rep = super(StudentsSerializer, self).to_representation(instance)
        rep['class_name'] = instance.class_name.name
        return rep


class StaffSerializer(serializers.ModelSerializer):
    subject_details = serializers.SerializerMethodField()
    class_details = serializers.SerializerMethodField()
    class Meta:
        model= Staff
        fields ="__all__"

        
    def get_subject_details(self, obj):
        subject_objects = obj.subjects.all()
        return SubjectSerializer(subject_objects, many = True).data
    
    def get_class_details(self, obj):
        return [class_name.name for class_name in obj.class_name.all()]
    

class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fees
        fields = ['id', 'student_name', 'total_fee', 'fee_paid', 'balance']
    def to_representation(self, instance):
        rep = super(FeesSerializer, self).to_representation(instance)
        rep['student_name'] = instance.student_name.name
        return rep

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =super().get_token(user)
        
        token['username'] = user.email
        return token