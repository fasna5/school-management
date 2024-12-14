
from django import forms
from saccounts.models import Student
from django.contrib.auth.forms import UserCreationForm
from saccounts.models import CustomUser,District,State,Country_Codes

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField( max_length=150, required=True)
    last_name = forms.CharField( max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=255, required=True)
    landmark = forms.CharField(max_length=255, required=False)
    place = forms.CharField(max_length=20, required=False)
    pin_code = forms.CharField(max_length=10, required=True)
    watsapp = forms.CharField(max_length=15, required=False)
    district = forms.ModelChoiceField(queryset=District.objects.all(), required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False)
    country_code = forms.ModelChoiceField(queryset=Country_Codes.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email', 'phone_number', 'address', 'landmark', 'place', 'pin_code', 'watsapp', 'district', 'state', 'country_code', 'password1', 'password2']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'class_field', 'division', 'roll_number', 'profile_image', 'id_number', 'about']
