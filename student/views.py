from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import AddStudentSerializer,StudentSerializer
from saccounts.models import CustomUser, Student
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class AddStudentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddStudentSerializer(data=request.data)

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


class StudentView(APIView):
    permission_classes = [IsAuthenticated]  # Protecting the view with authentication

    def get(self, request):
        user = request.user
        try:
            # Get the student object using the authenticated user
            student = Student.objects.get(user=user)
            # Serialize the student object along with the associated CustomUser data
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'Student updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            # Get the student object using the authenticated user
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'Student partially updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
        # Get the student object using the authenticated user
            student = Student.objects.get(user=request.user)

        # Delete the associated CustomUser object
            user = student.user
            student.delete()  # Delete the student object first (to avoid foreign key issues)

        # Also delete the related CustomUser
            user.delete()

            return Response({'status': 'Student and associated user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
        # Handle unexpected errors here
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
