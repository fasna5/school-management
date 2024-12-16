from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import AddStaffSerializer,StaffSerializer,EmailSerializer,AddStudentSerializerAdmin,StudentAdminSerializer
from saccounts.models import CustomUser, Student,Staff
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
class AddStaffView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAdminUser] 
    def post(self, request):
        serializer = AddStaffSerializer(data=request.data)

        # Validate the serializer
        if serializer.is_valid():
            # Extract the validated data from the serializer
            validated_data = serializer.validated_data

            # Check if email already exists
            if CustomUser.objects.filter(email=validated_data.get('email')).exists():
                return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if phone number already exists
            if CustomUser.objects.filter(phone_number=validated_data.get('phone_number')).exists():
                return Response({'error': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Create the user
                user = CustomUser.objects.create(
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    address=validated_data.get('address'),
                    landmark=validated_data.get('landmark'),
                    place=validated_data.get('place'),
                    pin_code=validated_data.get('pin_code'),
                    watsapp=validated_data.get('watsapp'),
                    district=validated_data.get('district'),
                    state=validated_data.get('state'),
                    email=validated_data.get('email'),
                    phone_number=validated_data.get('phone_number'),
                    country_code=validated_data.get('country_code'),
                    is_staff=validated_data.get('is_staff'),
                    is_librarian=validated_data.get('is_librarian')
                )

                # Set the password for the user
                password = validated_data.get('password')
                user.set_password(password)
                user.save()

                # Create the student record
                staff = Staff.objects.create(
                    user=user,
                    date_of_birth=validated_data.get('date_of_birth'),
                    subjects=validated_data.get('subjects'),
                    profile_image=validated_data.get('profile_image'),  # Optional field
                    id_number=validated_data.get('id_number'),
                    about=validated_data.get('about')  # Optional field
                )

                return Response({
                    'status': 'Staff created successfully',
                    'staff_id_number': staff.id_number
                }, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # If there's an IntegrityError (such as duplicate email or phone number)
                return Response({'error': 'Email or Phone Number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # Handle unexpected errors here
                print(e)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffView(APIView):
    permission_classes = [IsAdminUser]  # Protecting the view with authentication

    def get(self, request):
        #user = request.user
        try:
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
               user_email = serializer.validated_data['email']  
              
               staff = Staff.objects.get(user__email=user_email)
            # Serialize the student object along with the associated CustomUser data
               serializer = StaffSerializer(staff)
               return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            serializer = EmailSerializer(data=request.data)  # Email validation
            if serializer.is_valid():
                user_email = serializer.validated_data['email']
                staff = Staff.objects.get(user__email=user_email)  # Find the staff by email
            
                staffserializer = StaffSerializer(staff, data=request.data)  # Create Staff serializer with data
            
                if staffserializer.is_valid():
                    staffserializer.save()  # Save the updated staff data
                    return Response({'status': 'Staff updated successfully'}, status=status.HTTP_200_OK)
                return Response(staffserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Staff.DoesNotExist:  # Catch Staff.DoesNotExist instead of Student
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
             # Step 1: Validate the email
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                user_email = serializer.validated_data['email']
                staff = Staff.objects.get(user__email=user_email)  # Find the staff by email
            
            # Step 2: Partial update using StaffSerializer
                staffserializer = StaffSerializer(staff, data=request.data, partial=True)  # partial=True allows partial updates
            
                if staffserializer.is_valid():
                     staffserializer.save()  # Save the updated staff data
                     return Response({'status': 'Staff updated successfully'}, status=status.HTTP_200_OK)
            
                return Response(staffserializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        try:
        # Step 1: Validate the email
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                user_email = serializer.validated_data['email']
                staff = Staff.objects.get(user__email=user_email)  # Find the staff by email
            
            # Step 2: Delete the associated CustomUser and the staff member
                user = staff.user  # Get the associated CustomUser
            
            # Delete the CustomUser (this will also delete the related staff member due to cascading)
                staff.delete()  # Delete the staff resource
                user.delete()  # Delete the associated CustomUser
            
                return Response({'status': 'Staff and associated CustomUser deleted successfully'}, status=status.HTTP_200_OK)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Staff.DoesNotExist:
           return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
    
        except Exception as e:
           return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddStudentAdminView(APIView):
    permission_classes = [IsAdminUser] 

    def post(self, request):
        serializer = AddStudentSerializerAdmin(data=request.data)

        # Validate the serializer
        if serializer.is_valid():
            # Extract the validated data from the serializer
            validated_data = serializer.validated_data

            # Check if email already exists
            if CustomUser.objects.filter(email=validated_data.get('email')).exists():
                return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if phone number already exists
            if CustomUser.objects.filter(phone_number=validated_data.get('phone_number')).exists():
                return Response({'error': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Create the user
                user = CustomUser.objects.create(
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    address=validated_data.get('address'),
                    landmark=validated_data.get('landmark'),
                    place=validated_data.get('place'),
                    pin_code=validated_data.get('pin_code'),
                    watsapp=validated_data.get('watsapp'),
                    district=validated_data.get('district'),
                    state=validated_data.get('state'),
                    email=validated_data.get('email'),
                    phone_number=validated_data.get('phone_number'),
                    country_code=validated_data.get('country_code'),
                    is_student=validated_data.get('is_student')
                )

                # Set the password for the user
                password = validated_data.get('password')
                user.set_password(password)
                user.save()

                # Create the student record
                student = Student.objects.create(
                    user=user,
                    date_of_birth=validated_data.get('date_of_birth'),
                    class_field=validated_data.get('class_field'),
                    division=validated_data.get('division'),
                    roll_number=validated_data.get('roll_number'),
                    profile_image=validated_data.get('profile_image'),  # Optional field
                    id_number=validated_data.get('id_number'),
                    about=validated_data.get('about')  # Optional field
                )

                return Response({
                    'status': 'Student created successfully',
                    'student_id_number': student.id_number
                }, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # If there's an IntegrityError (such as duplicate email or phone number)
                return Response({'error': 'Email or Phone Number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # Handle unexpected errors here
                print(e)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentAdminView(APIView):
    permission_classes = [IsAdminUser]  # Protecting the view with authentication

    def get(self, request):
        #user = request.user
        try:
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
               user_email = serializer.validated_data['email']  
              
               student = Student.objects.get(user__email=user_email)
            # Serialize the student object along with the associated CustomUser data
               serializer = StudentAdminSerializer(student)
               return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            serializer = EmailSerializer(data=request.data)  # Email validation
            if serializer.is_valid():
                user_email = serializer.validated_data['email']
                student = Student.objects.get(user__email=user_email)  # Find the staff by email
            
                studentadminserializer = StudentAdminSerializer(student, data=request.data)  # Create Staff serializer with data
            
                if studentadminserializer.is_valid():
                    studentadminserializer.save()  # Save the updated staff data
                    return Response({'status': 'Student updated successfully'}, status=status.HTTP_200_OK)
                return Response(studentadminserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Student.DoesNotExist:  # Catch Staff.DoesNotExist instead of Student
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
             # Step 1: Validate the email
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                user_email = serializer.validated_data['email']
                student = Student.objects.get(user__email=user_email)  # Find the staff by email
            
            # Step 2: Partial update using StaffSerializer
                studentadminserializer = StudentAdminSerializer(student, data=request.data, partial=True)  # partial=True allows partial updates
            
                if studentadminserializer.is_valid():
                     studentadminserializer.save()  # Save the updated staff data
                     return Response({'status': 'Student updated successfully'}, status=status.HTTP_200_OK)
            
                return Response(studentadminserializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        try:
        # Step 1: Validate the email
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                user_email = serializer.validated_data['email']
                student = Student.objects.get(user__email=user_email)  # Find the staff by email
            
            # Step 2: Delete the associated CustomUser and the staff member
                user = student.user  # Get the associated CustomUser
            
            # Delete the CustomUser (this will also delete the related staff member due to cascading)
                student.delete()  # Delete the staff resource
                user.delete()  # Delete the associated CustomUser
            
                return Response({'status': 'Student and associated CustomUser deleted successfully'}, status=status.HTTP_200_OK)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Student.DoesNotExist:
           return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
        except Exception as e:
           return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
