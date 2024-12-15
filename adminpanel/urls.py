from django.urls import path
from .views import * 


urlpatterns=[
    
    
    path('addstaff/',AddStaffView.as_view(),name='addstaff'),
    
    
]