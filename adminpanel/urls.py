from django.urls import path
from .views import * 


urlpatterns=[
    
    
    path('addstaff/',AddStaffView.as_view(),name='addstaff'),
    path('staffedit/',StaffView.as_view(),name='staffedit'),
    
    
]