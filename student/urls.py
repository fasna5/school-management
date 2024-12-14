from django.urls import path
from student.views import AddStudentView,StudentView


urlpatterns=[
    
    
    path('add_student/',AddStudentView.as_view(),name='add_student'),
    path('studentedit/',StudentView.as_view(),name='studentedit'),
    
    
    
]