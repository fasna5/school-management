from rest_framework import serializers
from saccounts.models import Country_Codes,CustomUser,State,District,Student,Staff


class AddStaffSerializer(serializers.Serializer):
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
    is_staff = serializers.BooleanField(default=False)
    is_librarian=serializers.BooleanField(default=False)
    date_of_birth=serializers.DateField(format="%Y-%m-%d")
    subjects = serializers.ChoiceField(choices=[
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Maths', 'Maths'),
        ('librarian','librarian')
    ]) 
     
    
    profile_image = serializers.ImageField(required = False)
    id_number=serializers.CharField(max_length=50)
    about = serializers.CharField(max_length = 255)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address','landmark','pin_code','watsapp','password','place','district', 'state', 'country_code', 'is_staff','is_librarian']

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField() 
class StaffSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Staff
        fields = [
            'id',
            'user',
            'date_of_birth',
            'subjects',
            'profile_image',
            'id_number',
            'about'
        ]

    def update(self, instance, validated_data):
        # Extract the user data from the request
        user_data = validated_data.pop('user', None)

        # Update student data
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.subjects = validated_data.get('subjects', instance.subjects)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.id_number = validated_data.get('id_number', instance.id_number)
        instance.about = validated_data.get('about', instance.about)

        # Update user data only if present in the request
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)

            # Only update email if it is provided and different from the existing one
            new_email = user_data.get('email', None)
            if new_email and new_email != user.email:
                # Validate if the email is different and exists already
                if CustomUser.objects.filter(email=new_email).exists():
                    raise serializers.ValidationError({'email': ['User with this email already exists.']})
                user.email = new_email

            # Only update phone_number if it is provided and different from the existing one
            new_phone_number = user_data.get('phone_number', None)
            if new_phone_number and new_phone_number != user.phone_number:
                # Validate if the phone_number is different and exists already
                if CustomUser.objects.filter(phone_number=new_phone_number).exists():
                    raise serializers.ValidationError({'phone_number': ['User with this phone number already exists.']})
                user.phone_number = new_phone_number

            # Handle other fields (only update them if present)
            user.password = user_data.get('password', user.password)  # Handle password separately
            user.address = user_data.get('address', user.address)
            user.landmark = user_data.get('landmark', user.landmark)
            user.pin_code = user_data.get('pin_code', user.pin_code)
            user.watsapp = user_data.get('watsapp', user.watsapp)
            user.place = user_data.get('place', user.place)
            user.district = user_data.get('district', user.district)
            user.state = user_data.get('state', user.state)
            user.country_code = user_data.get('country_code', user.country_code)
            user.is_staff = user_data.get('is_staff', user.is_staff)
            user.is_librarian = user_data.get('is_librarian', user.is_librarian)

            # Save the user instance
            user.save()

        # Save the updated student instance
        instance.save()

        return instance
