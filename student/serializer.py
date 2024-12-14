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


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id', 
            'user', 
            'date_of_birth', 
            'class_field', 
            'division', 
            'roll_number', 
            'profile_image', 
            'id_number', 
            'about'
        ]
        
    def update(self, instance, validated_data):
        """
        This method is called for both PUT and PATCH requests.
        It will update the existing instance with the validated data.
        """
        # Update fields if they are provided
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.class_field = validated_data.get('class_field', instance.class_field)
        instance.division = validated_data.get('division', instance.division)
        instance.roll_number = validated_data.get('roll_number', instance.roll_number)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.id_number = validated_data.get('id_number', instance.id_number)
        instance.about = validated_data.get('about', instance.about)
        
        instance.save()
        return instance

    
    