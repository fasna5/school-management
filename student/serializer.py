from rest_framework import serializers
from saccounts.models import Country_Codes,CustomUser,State,District,Student


class AddStudentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name=serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=30)
    landmark = serializers.CharField(max_length = 255)
    place = serializers.CharField(max_length = 20)
    pin_code = serializers.CharField(max_length=10)
    watsapp=serializers.CharField(max_length = 255)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length = 15)
    country_code = serializers.PrimaryKeyRelatedField(queryset=Country_Codes.objects.all())
    password = serializers.CharField(max_length = 50)
    is_student = serializers.BooleanField(default=False)
    date_of_birth=serializers.DateField(format="%Y-%m-%d")
    class_field=serializers.CharField(max_length=50) 
    division=serializers.CharField(max_length=50) 
    roll_number=serializers.IntegerField()
    profile_image = serializers.ImageField(required = False)
    id_number=serializers.CharField(max_length=50)
    about = serializers.CharField(max_length = 255)
    
    