from django.urls import path
from student.views import AddStudentView


urlpatterns=[
    
    
    path('add_student/',AddStudentView.as_view(),name='add_student'),
    
    
    
]