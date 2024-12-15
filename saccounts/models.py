from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Permission,Group
from django.forms import ValidationError
from django.utils import timezone
import random
from django.core.validators import RegexValidator
import phonenumbers
from django.conf import settings
import uuid
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError
import uuid

phone_regex = RegexValidator(
        regex=r'^\d{9,15}$', 
        message="Phone number must be between 9 and 15 digits."
    )

def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:  # 10 MB
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    return value

class Country_Codes(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    calling_code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.country_name} ({self.calling_code})"
    
    class Meta:
        ordering = ['calling_code']

class State(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name

GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
]
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username=None
    created_at = models.DateTimeField(auto_now_add=True)
    # Role-based fields
    is_student = models.BooleanField(default=False)
    
    
    # Admin-related fields
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)


    # Any other fields common to both roles
    
    address = models.CharField(max_length=30)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=20,blank=True,null=True)
    pin_code = models.CharField(max_length=10)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    joining_date = models.DateField(null=True,blank=True)
    watsapp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True,validators=[phone_regex], null=True, blank=True)
    country_code = models.ForeignKey('Country_Codes', on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    
    
    groups = models.ManyToManyField(
        Group,
        related_name='app1_user_groups',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Override user_permissions field with a unique related_name
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='app1_user_permissions'  # Add a unique related_name
    )
    
    def __str__(self):
        return self.email 

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    


    objects = CustomUserManager()

class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student',null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    class_field=models.CharField(max_length=50, blank=True, null=True) 
    division=models.CharField(max_length=50, blank=True, null=True) 
    roll_number=models.IntegerField(max_length=15,blank=True,null=True)
    profile_image=profile_image = models.ImageField(upload_to='d-profile-images/', null=True, blank=True, validators=[validate_file_size])  # Profile image field
    id_number=models.CharField(max_length=50, blank=True, null=True)  # ID number field
    about=models.TextField(null=True,blank=True)

    

class Staff(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='staff',null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # Define choices for the dropdown
    CATEGORY_CHOICES = [
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Maths', 'Maths'),
        ('librarian','librarian')
    ]
    subjects = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,  # Dropdown choices
        default='Physics',     # Default category
    )
    profile_image=profile_image = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])  # Profile image field
    id_number=models.CharField(max_length=50, blank=True, null=True)  # ID number field
    about=models.TextField(null=True,blank=True)


class LibraryForm(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)
    book_name=models.CharField(max_length=255, blank=True, null=True)
    borrow_date=models.DateField(null=True, blank=True)
    return_date=models.DateField(null=True, blank=True)
    status= models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

class FeesForm(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.PROTECT)
    fee_type=models.CharField(max_length=255, blank=True, null=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    payment_date=models.DateField(null=True, blank=True)
    remarks=models.TextField(null=True,blank=True)
