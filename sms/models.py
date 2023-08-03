import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from .managers import CustomUserManager
GENDER_CHOICES = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
    ('others', 'not specified'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    # These fields tie to the roles!
    TEACHER = 1
    STUDENT = 2


    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=4, null=True)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.subject_name

class Clss(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject)
    subject_details = models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Students(models.Model):
    name = models.CharField(max_length=100)
    roll_no  = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[
            MaxValueValidator(17),
            MinValueValidator(4)
        ])
    date_of_birth = models.DateField()
    mothers_mobile_no = models.BigIntegerField(unique=True, null=True, validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ])
    fathers_mobile_no = models.BigIntegerField(unique=True, validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    date_of_joining = models.DateField(null=True)
    class_name = models.ForeignKey(Clss, on_delete=models.CASCADE)
    photo = models.ImageField(max_length=255)
    
    
    
    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    staff_id  = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100)

    mobile_no = models.BigIntegerField(unique=True, validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ])
    alternate_mobile_no = models.BigIntegerField(unique=True, null=True, validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField(null=True)
    subjects = models.ManyToManyField(Subject)
    subject_details = models.IntegerField(null=True)
    class_name = models.ManyToManyField(Clss)
    class_details = models.IntegerField(null=True)
    photo = models.ImageField(max_length=255)
    def __str__(self):
        return self.name

class Fees(models.Model):
    student_name=models.ForeignKey(Students, on_delete=models.CASCADE, related_name='students')
    total_fee = models.FloatField()
    fee_paid = models.FloatField()
    balance = models.FloatField()


# Create your models here.
