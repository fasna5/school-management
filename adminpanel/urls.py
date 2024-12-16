from django.urls import path
from .views import * 


urlpatterns=[
    
    
    path('addstaff/',AddStaffView.as_view(),name='addstaff'),
    path('staffedit/',StaffView.as_view(),name='staffedit'),
    path('addstudentadmin/',AddStudentAdminView.as_view(),name='addstudentadmin'),
    path('studenteditadmin/',StudentAdminView.as_view(),name='studenteditadmin'),
    
    
]