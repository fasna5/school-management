from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(LibraryForm)
admin.site.register(FeesForm)
admin.site.register(Country_Codes)
admin.site.register(State)
admin.site.register(District)